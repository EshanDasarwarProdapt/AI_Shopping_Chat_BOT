from sqlalchemy import Column, Integer, String, Float, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    brand = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    specifications = Column(JSON) # e.g. {"RAM": "16GB", "Storage": "512GB SSD"}
    image_url = Column(String)
    embedding = Column(JSON) # Array of floats

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    browsing_history = Column(JSON) # list of product ids
    purchase_history = Column(JSON) # list of product ids

class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    history = Column(JSON)
