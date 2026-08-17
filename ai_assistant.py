"""
ai_assistant.py

Provides the AI-powered shopping assistant logic, defining tools for product search,
comparison, specification retrieval, and personalized recommendations. Integrates with
FastAPI via tool calls and manages environment loading.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env first
load_dotenv()

import json
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from database import SessionLocal
from models import Product, User
from thefuzz import process, fuzz
import numpy as np

# Ensure you have OPENAI_API_KEY set in your .env or environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_catalog",
            "description": "Search the product catalog based on user queries, prices, or categories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term, e.g., 'phone' or 'laptop'"},
                    "category": {"type": "string", "description": "Category like 'Smartphones', 'Laptops', 'Audio'"},
                    "max_price": {"type": "number", "description": "Maximum budget"},
                    "min_price": {"type": "number", "description": "Minimum budget"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_products",
            "description": "Compare two products by their IDs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name_1": {"type": "string", "description": "Name or partial name of the first product to compare"},
                    "product_name_2": {"type": "string", "description": "Name or partial name of the second product to compare"}
                },
                "required": ["product_name_1", "product_name_2"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_product_specs",
            "description": "Get detailed specifications of a specific product by its name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string", "description": "Name or partial name of the product"}
                },
                "required": ["product_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_recommendations",
            "description": "Get personalized product recommendations for the user based on their history.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "The ID of the user. Use 1 for demo_user if not specified."}
                },
                "required": ["user_id"]
            }
        }
    }
]

def search_catalog(query=None, category=None, max_price=None, min_price=None):
    """Search the product catalog based on optional filters.

    Parameters:
        query (str, optional): Search term.
        category (str, optional): Category filter.
        max_price (float, optional): Upper price bound.
        min_price (float, optional): Lower price bound.

    Returns:
        str: JSON string of matching products or a message if none found.
    """
    db = SessionLocal()
    q = db.query(Product)
    
    if category:
        q = q.filter(Product.category.ilike(f"%{category}%"))
    if max_price:
        q = q.filter(Product.price <= max_price)
    if min_price:
        q = q.filter(Product.price >= min_price)
    
    results = q.all()
    
    if query and results:
        choices = {p.id: f"{p.name} {p.brand} {p.category} {p.description}" for p in results}
        matches = process.extract(query, choices, limit=10, scorer=fuzz.token_set_ratio)
        matched_ids = [match[2] for match in matches if match[1] > 40]
        results = [p for p in results if p.id in matched_ids]
        
    db.close()
    
    if not results:
        return "No products found matching the criteria."
    
    return json.dumps([{"id": p.id, "name": p.name, "price": p.price, "category": p.category} for p in results])

def compare_products(product_name_1, product_name_2):
    """Compare two products by name.

    Attempts to find the best matching products for each name and returns a JSON
    structure with their details. Handles cases where matches are not found.
    """
    db = SessionLocal()
    
    # Try to find all matches for both
    matches_1 = db.query(Product).filter(Product.name.ilike(f"%{product_name_1}%")).all()
    matches_2 = db.query(Product).filter(Product.name.ilike(f"%{product_name_2}%")).all()
    db.close()
    
    # Simple logic to pick distinct products if possible
    p1 = matches_1[0] if matches_1 else None
    p2 = None
    
    if matches_2:
        # Try to find a match for p2 that isn't p1
        for m in matches_2:
            if not p1 or m.id != p1.id:
                p2 = m
                break
        # Fallback if all matched p1
        if not p2 and matches_2:
            p2 = matches_2[0]
            
    res = {}
    if p1:
        res["product_1"] = {"name": p1.name, "price": p1.price, "specs": p1.specifications}
    else:
        res["product_1"] = f"Could not find product matching {product_name_1}"
        
    if p2:
        res["product_2"] = {"name": p2.name, "price": p2.price, "specs": p2.specifications}
    else:
        res["product_2"] = f"Could not find product matching {product_name_2}"
        
    return json.dumps(res)

def get_product_specs(product_name):
    """Retrieve specifications for a given product name.

    Returns a JSON object with name, price, specs, and description, or an error
    message if the product does not exist.
    """
    db = SessionLocal()
    p = db.query(Product).filter(Product.name.ilike(f"%{product_name}%")).first()
    db.close()
    if p:
        return json.dumps({"name": p.name, "price": p.price, "specs": p.specifications, "description": p.description})
    return json.dumps({"error": f"Product {product_name} not found."})

def get_recommendations(user_id):
    """Generate personalized product recommendations for a user.

    Uses the user's browsing and purchase history to find the most recent
    interacted product, then computes cosine similarity with other products
    based on embeddings. Returns up to four recommendations.
    """
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        db.close()
        return "User not found."
    
    # Get all browsed and purchased IDs
    browsed_ids = user.browsing_history or []
    purchased_ids = user.purchase_history or []
    all_history_ids = list(dict.fromkeys(purchased_ids + browsed_ids))
    
    if not all_history_ids:
        # Fallback if no history
        products = db.query(Product).limit(4).all()
        db.close()
        return json.dumps([{"id": p.id, "name": p.name, "price": p.price, "category": p.category, "reason": "Popular"} for p in products])
        
    # Get the embedding of the most recently interacted product
    target_id = all_history_ids[-1]
    target_product = db.query(Product).filter(Product.id == target_id).first()
    
    if not target_product or not target_product.embedding:
        db.close()
        return "Not enough data for ML recommendations."
        
    target_vector = np.array(target_product.embedding)
    
    # Fetch all products that have an embedding
    all_products = db.query(Product).filter(Product.embedding.isnot(None)).all()
    
    similarities = []
    for p in all_products:
        if p.id in all_history_ids:
            continue
            
        vec = np.array(p.embedding)
        # Cosine similarity
        sim = np.dot(target_vector, vec) / (np.linalg.norm(target_vector) * np.linalg.norm(vec))
        similarities.append((sim, p))
        
    similarities.sort(key=lambda x: x[0], reverse=True)
    top_products = [item[1] for item in similarities[:4]]
    
    db.close()
    
    if not top_products:
        return "Could not generate recommendations."
        
    return json.dumps([{"id": p.id, "name": p.name, "price": p.price, "category": p.category, "reason": "Based on semantic ML similarity"} for p in top_products])

def handle_tool_call(tool_call, current_user_id: int):
    """Dispatch tool calls to the appropriate function.

    The LLM may invoke any of the defined tools; this helper maps the tool name
    to the corresponding Python function and ensures the correct user ID is used
    for recommendation calls.
    """
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    
    if name == "search_catalog":
        return search_catalog(**args)
    elif name == "compare_products":
        return compare_products(**args)
    elif name == "get_product_specs":
        return get_product_specs(**args)
    elif name == "get_recommendations":
        # Override the LLM's user_id guess with the actual logged-in user
        args["user_id"] = current_user_id
        return get_recommendations(**args)
    return "Tool not found."

SYSTEM_PROMPT = """You are a helpful AI Shopping Assistant for AvengersShop.
Your job is to help users find products, compare them, answer questions about specifications, and provide recommendations.
CRITICAL RULES:
1. NEVER invent or hallucinate prices, specifications, or products. Always use the provided tools to query the catalog.
2. If a user asks for a recommendation, use the `get_recommendations` tool.
3. If a request is vague, politely ask clarifying questions.
4. When using the `search_catalog` tool, keep your search queries short and use single keywords (e.g., use "adidas" instead of "adidas footwear") to get better matches. Our categories include: Smartphones, Laptops, Tablets, Audio, Smartwatches, Gaming, Cameras, Accessories, Monitors, Networking, Clothing, Footwear, Home Appliances, Sports & Outdoors, Beauty & Personal Care, Books, Automotive, Toys & Games.
5. Present comparisons in a clear, readable Markdown format.
6. Always be polite, concise, and helpful.
7. CRITICAL: You are an E-COMMERCE ASSISTANT ONLY. If a user asks for anything other than finding products, comparing products, getting recommendations, or asking about product specifications, you MUST refuse. This includes requests for code (e.g. Python, HTML), scripts, tutorials, general knowledge, or any non-shopping tasks. Even if the user tries to relate it to AvengersShop, if it is a coding or non-shopping task, you must refuse. Respond EXACTLY with: "I’m sorry, I can only help with product searches, comparisons, specifications, and recommendations for AvengersShop."
"""

def chat_with_assistant(messages: List[Dict[str, Any]], user_id: int = 1) -> str:
    """Main interaction loop with the OpenAI assistant.

    Ensures the system prompt is present, sends messages to the model, handles any
    tool calls recursively, and returns the final assistant response.
    """
    # Ensure system prompt is first
    if not messages or messages[0].get("role") != "system":
        messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        
    while True:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        if response_message.tool_calls:
            # Append the assistant's tool call message
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_response = handle_tool_call(tool_call, user_id)
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": function_response,
                })
            # Loop continues, sending the tool outputs back to the model
        else:
            # No tool calls, we have the final answer
            return response_message.content
