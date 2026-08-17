"""backfill_embeddings.py

Utility script to generate OpenAI text embeddings for all products in the DemoShop catalog and store them in the SQLite database. Each product receives a 1536‑dimensional vector (stored as JSON) that can later be used for semantic similarity calculations.
"""
import os
import json
from dotenv import load_dotenv

# Load environment variables (especially OPENAI_API_KEY) before anything else.
load_dotenv()

from openai import OpenAI
from database import SessionLocal
from models import Product

# Initialise the OpenAI client using the API key from the environment.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str) -> list[float]:
    """
    Retrieve a semantic embedding for the given text using OpenAI's
    `text-embedding-3-small` model.

    Args:
        text: The string to embed (typically a concatenation of product
              name, brand, category and description).

    Returns:
        A list of floats representing the embedding vector.
    """
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def backfill():
    """Iterate over every product, generate embeddings, and persist them.

    The script is idempotent – it skips products that already have an embedding.
    Progress is printed to the console for monitoring.
    """
    db = SessionLocal()
    products = db.query(Product).all()
    total = len(products)

    print(f"Starting to backfill {total} products...")

    count = 0
    for product in products:
        # Skip products that already have an embedding.
        if product.embedding is not None:
            continue

        # Create a single text blob that captures the main product attributes.
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
