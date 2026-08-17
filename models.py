"""models.py

Defines SQLAlchemy ORM models for the DemoShop application, including Product,
User, and ChatSession. These models map to the SQLite database and are used for
data persistence throughout the app.
"""

from sqlalchemy import Column, Integer, String, Float, JSON
from sqlalchemy.orm import declarative_base

# Base class for all ORM models.
Base = declarative_base()

class Product(Base):
    """Catalog product model.

    Attributes:
        id: Primary key.
        name: Product title.
        category: High‑level category (e.g., "Shoes").
        brand: Manufacturer name.
        price: Monetary value.
        description: Free‑form description text.
        specifications: JSON blob for technical specs (e.g., RAM, Storage).
        image_url: URL to product image.
        embedding: JSON array storing a 1536‑dimensional vector from OpenAI.
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    brand = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    specifications = Column(JSON)  # e.g. {"RAM": "16GB", "Storage": "512GB SSD"}
    image_url = Column(String)
    embedding = Column(JSON)  # Stores the OpenAI embedding vector for semantic similarity.

class User(Base):
    """Application user model.

    Attributes:
        id: Primary key.
        username: Unique login name.
        password_hash: Bcrypt hash of the password.
        browsing_history: JSON list of product IDs the user has viewed.
        purchase_history: JSON list of product IDs the user has bought.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    browsing_history = Column(JSON)  # list of product ids
    purchase_history = Column(JSON)  # list of product ids

class ChatSession(Base):
    """Persisted chat session for a user.

    Attributes:
        id: Primary key.
        user_id: Foreign key to the owning user.
        history: JSON array of message objects representing the conversation.
    """
    __tablename__ = 'chat_sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    history = Column(JSON)
