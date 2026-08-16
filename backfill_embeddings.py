import os
import json
from dotenv import load_dotenv

# Ensure dotenv is loaded first
load_dotenv()

from openai import OpenAI
from database import SessionLocal
from models import Product

# Ensure you have OPENAI_API_KEY set in your .env or environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def backfill():
    db = SessionLocal()
    products = db.query(Product).all()
    total = len(products)
    
    print(f"Starting to backfill {total} products...")
    
    count = 0
    for product in products:
        # Check if embedding already exists
        if product.embedding is not None:
            continue
            
        # Combine text for embedding
        text_to_embed = f"{product.name} {product.brand} {product.category} {product.description}"
        try:
            vector = get_embedding(text_to_embed)
            product.embedding = vector
            db.commit()
            count += 1
            if count % 10 == 0:
                print(f"Processed {count}/{total} products...")
        except Exception as e:
            print(f"Failed on product {product.id}: {e}")
            break
            
    print(f"Finished backfilling {count} new embeddings.")
    db.close()

if __name__ == "__main__":
    backfill()
