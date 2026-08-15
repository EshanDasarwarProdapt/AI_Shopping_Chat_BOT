import os
import json
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from database import SessionLocal
from models import Product, User
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

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
    db = SessionLocal()
    q = db.query(Product)
    if category:
        q = q.filter(Product.category.ilike(f"%{category}%"))
    if query:
        q = q.filter(Product.name.ilike(f"%{query}%") | Product.description.ilike(f"%{query}%"))
    if max_price:
        q = q.filter(Product.price <= max_price)
    if min_price:
        q = q.filter(Product.price >= min_price)
    
    results = q.all()
    db.close()
    
    if not results:
        return "No products found matching the criteria."
    
    return json.dumps([{"id": p.id, "name": p.name, "price": p.price, "category": p.category} for p in results])

def compare_products(product_name_1, product_name_2):
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
    db = SessionLocal()
    p = db.query(Product).filter(Product.name.ilike(f"%{product_name}%")).first()
    db.close()
    if p:
        return json.dumps({"name": p.name, "price": p.price, "specs": p.specifications, "description": p.description})
    return json.dumps({"error": f"Product {product_name} not found."})

def get_recommendations(user_id):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        db.close()
        return "User not found."
    
    # Simple recommendation: fetch products they browsed OR purchased
    browsed_ids = user.browsing_history or []
    purchased_ids = user.purchase_history or []
    all_ids = list(set(browsed_ids + purchased_ids))
    
    if not all_ids:
        db.close()
        return "No browsing or purchase history to base recommendations on."
        
    history_products = db.query(Product).filter(Product.id.in_(all_ids)).all()
    categories = list(set([p.category for p in history_products]))
    brands = list(set([p.brand for p in history_products]))
    
    from sqlalchemy.sql.expression import func
    
    recommendations = db.query(Product).filter(
        (Product.category.in_(categories)) | (Product.brand.in_(brands)),
        ~Product.id.in_(all_ids)
    ).order_by(func.random()).limit(5).all()
    
    db.close()
    
    if not recommendations:
        return "No new recommendations found for your preferred categories."
        
    return json.dumps([{"name": p.name, "price": p.price, "category": p.category, "brand": p.brand} for p in recommendations])

def handle_tool_call(tool_call, current_user_id: int):
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

SYSTEM_PROMPT = """You are a helpful AI Shopping Assistant for DemoShop.
Your job is to help users find products, compare them, answer questions about specifications, and provide recommendations.
CRITICAL RULES:
1. NEVER invent or hallucinate prices, specifications, or products. Always use the provided tools to query the catalog.
2. If a user asks for a recommendation, use the `get_recommendations` tool.
3. If a request is vague, politely ask clarifying questions.
4. When using the `search_catalog` tool, keep your search queries short and use single keywords (e.g., use "adidas" instead of "adidas footwear") to get better matches. Our categories include: Smartphones, Laptops, Tablets, Audio, Smartwatches, Gaming, Cameras, Accessories, Monitors, Networking, Clothing, Footwear, Home Appliances, Sports & Outdoors, Beauty & Personal Care, Books, Automotive, Toys & Games.
5. Present comparisons in a clear, readable Markdown format.
6. Always be polite, concise, and helpful.
"""

def chat_with_assistant(messages: List[Dict[str, Any]], user_id: int = 1) -> str:
    # Ensure system prompt is first
    if not messages or messages[0].get("role") != "system":
        messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        
    response = client.chat.completions.create(
        model="gpt-5-nano",  # or gpt-3.5-turbo
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
            
        # Second call to get final response
        second_response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=messages,
        )
        return second_response.choices[0].message.content
    else:
        return response_message.content
