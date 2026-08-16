from fastapi import FastAPI, Depends, Request, Form, Response, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from database import get_db, init_db
import json
import os
from dotenv import load_dotenv

# Ensure dotenv is loaded before anything else
load_dotenv()

from models import Product, User, ChatSession

from ai_assistant import chat_with_assistant
from passlib.context import CryptContext
from sqlalchemy.sql.expression import func
from thefuzz import process, fuzz

app = FastAPI(title="DemoShop AI Assistant")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Auth dependency
def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("session_user_id")
    if not user_id:
        return None
    return db.query(User).filter(User.id == int(user_id)).first()

def get_current_user_required(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user

# Initialize database
@app.on_event("startup")
def startup_event():
    init_db()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str
    user_id: int = 1
    session_id: int = 1

# --- Page Routes ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, category: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Product)
    if category:
        q = q.filter(Product.category == category)
    products = q.all()
    
    # Get all unique categories for the filter sidebar
    all_categories = [row[0] for row in db.query(Product.category).distinct().all()]
    
    user = get_current_user(request, db)
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "products": products, 
        "user": user,
        "categories": all_categories,
        "selected_category": category
    })

@app.get("/search", response_class=HTMLResponse)
async def search_page(request: Request, q: str = "", db: Session = Depends(get_db)):
    query = db.query(Product)
    if q:
        search_term = f"%{q}%"
        query = query.filter(
            Product.name.ilike(search_term) | 
            Product.description.ilike(search_term) | 
            Product.category.ilike(search_term) |
            Product.brand.ilike(search_term)
        )
    products = query.all()
    user = get_current_user(request, db)
    all_categories = [row[0] for row in db.query(Product.category).distinct().all()]
    return templates.TemplateResponse("index.html", {
        "request": request,
        "products": products,
        "user": user,
        "categories": all_categories,
        "selected_category": None,
        "search_query": q
    })

@app.get("/product/{product_id}", response_class=HTMLResponse)
async def view_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    user = get_current_user(request, db)
    
    if user and product:
        current_history = user.browsing_history or []
        if product.id in current_history:
            current_history.remove(product.id)
        current_history.append(product.id)
        current_history = current_history[-20:] # Keep last 20
        db.query(User).filter(User.id == user.id).update({"browsing_history": current_history})
        db.commit()
    
    # Related products from same category
    related = []
    if product:
        related = db.query(Product).filter(
            Product.category == product.category, 
            Product.id != product.id
        ).limit(4).all()
    
    return templates.TemplateResponse("product_details.html", {
        "request": request, 
        "product": product, 
        "user": user,
        "related_products": related
    })

@app.get("/cart", response_class=HTMLResponse)
async def view_cart(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    return templates.TemplateResponse("cart.html", {"request": request, "user": user})

@app.get("/checkout", response_class=HTMLResponse)
async def view_checkout(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("checkout.html", {"request": request, "user": user})

# --- Search API (for live search suggestions) ---

@app.get("/api/search")
def api_search(q: str = "", db: Session = Depends(get_db)):
    if not q or len(q) < 2:
        return []
        
    all_products = db.query(Product).all()
    # Create a searchable string for each product combining name, brand, and category
    choices = {p.id: f"{p.name} {p.brand} {p.category}" for p in all_products}
    
    # Extract top matches
    matches = process.extract(q, choices, limit=6, scorer=fuzz.token_set_ratio)
    
    # matches format: [(match_string, score, key), ...]
    matched_ids = [match[2] for match in matches if match[1] > 40]
    
    if not matched_ids:
        return []
        
    # Fetch original product objects in order of matches
    products = db.query(Product).filter(Product.id.in_(matched_ids)).all()
    products_by_id = {p.id: p for p in products}
    ordered_products = [products_by_id[pid] for pid in matched_ids if pid in products_by_id]
    
    return [{"id": p.id, "name": p.name, "price": p.price, "category": p.category, "image_url": p.image_url} for p in ordered_products]

# --- Auth Routes ---

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def post_login(response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password_hash):
        return RedirectResponse(url="/login?error=1", status_code=status.HTTP_302_FOUND)
    
    redirect_response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    redirect_response.set_cookie(key="session_user_id", value=str(user.id))
    return redirect_response

@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def post_register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        return RedirectResponse(url="/register?error=1", status_code=status.HTTP_302_FOUND)
    
    user = User(
        username=username,
        password_hash=pwd_context.hash(password),
        browsing_history=[],
        purchase_history=[]
    )
    db.add(user)
    db.commit()
    return RedirectResponse(url="/login?registered=1", status_code=status.HTTP_302_FOUND)

@app.get("/logout")
async def logout(response: Response):
    redirect_response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie("session_user_id")
    return redirect_response

# --- Dashboard ---

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        
    # Get order history
    purchased_ids = user.purchase_history or []
    orders = db.query(Product).filter(Product.id.in_(purchased_ids)).all()
    
    browsed_ids = user.browsing_history or []
    
    # Get recommendations using ML embeddings
    recommendations = []
    if orders or browsed_ids:
        all_ids = list(set([o.id for o in orders] + browsed_ids))
        if all_ids:
            target_id = all_ids[-1]
            target_product = db.query(Product).filter(Product.id == target_id).first()
            
            if target_product and target_product.embedding:
                import numpy as np
                target_vector = np.array(target_product.embedding)
                all_products = db.query(Product).filter(Product.embedding.isnot(None)).all()
                similarities = []
                for p in all_products:
                    if p.id in all_ids:
                        continue
                    vec = np.array(p.embedding)
                    # Cosine similarity
                    sim = np.dot(target_vector, vec) / (np.linalg.norm(target_vector) * np.linalg.norm(vec))
                    similarities.append((sim, p))
                
                similarities.sort(key=lambda x: x[0], reverse=True)
                recommendations = [item[1] for item in similarities[:4]]
        
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": user, 
        "orders": orders, 
        "recommendations": recommendations
    })

# --- Checkout API ---

class CheckoutRequest(BaseModel):
    items: List[int] # List of product IDs

@app.post("/api/checkout")
def checkout_endpoint(req: CheckoutRequest, db: Session = Depends(get_db), request: Request = None):
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Must be logged in to checkout")
        
    current_history = user.purchase_history or []
    current_history.extend(req.items)
    
    user.purchase_history = current_history
    # Force sqlalchemy update
    db.query(User).filter(User.id == user.id).update({"purchase_history": current_history})
    db.commit()
    
    return {"status": "success"}

# --- Product APIs ---

@app.get("/api/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.get("/api/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.id == product_id).first()

# --- Chat API ---

@app.get("/api/chat/history/{session_id}")
def get_chat_history(session_id: int, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if session and session.history:
        return session.history
    return []

@app.post("/api/chat")
def chat_endpoint(chat_request: ChatRequest, request: Request, db: Session = Depends(get_db)):
    # Get current user if logged in, otherwise default to 1 (guest/demo)
    user = get_current_user(request, db)
    actual_user_id = user.id if user else chat_request.user_id

    # Retrieve or create chat session
    session = db.query(ChatSession).filter(ChatSession.id == chat_request.session_id).first()
    
    if not session:
        session = ChatSession(id=chat_request.session_id, user_id=actual_user_id, history=[])
        db.add(session)
        db.commit()
        
    # We need to make sure history is a list
    history = session.history if session.history else []
    
    # Add user message
    user_message = {"role": "user", "content": chat_request.message}
    
    # Reconstruct messages for OpenAI
    ai_messages = []
    for msg in history:
        ai_messages.append(msg)
    ai_messages.append(user_message)
    
    # Call Assistant
    try:
        reply = chat_with_assistant(ai_messages, user_id=actual_user_id)
        
        # Save to history
        history.append(user_message)
        history.append({"role": "assistant", "content": reply})
        
        # Update DB
        session.history = history
        db.query(ChatSession).filter(ChatSession.id == session.id).update({"history": history})
        db.commit()
        
        return {"response": reply}
    except Exception as e:
        return {"response": f"Sorry, I encountered an error: {str(e)}"}
