# AI Shopping Assistant Chatbot

A professional, full-stack Python-based e-commerce web application featuring a sophisticated AI Shopping Assistant. The assistant helps users find products, compare options, answers specification questions, and gives personalized recommendations, completely grounded in real product data.

## 🚀 Features

- **Conversational AI Assistant:** Powered by OpenAI, it uses function-calling to query the database, recommend products, and parse user intent.
- **Dynamic Database:** Scaled catalog of **250 products** spanning 12 distinct categories (Tech, Footwear, Clothing, Home Appliances, etc.).
- **Smart Recommendations:** Uses both your browsing and purchase history to dynamically surface relevant new products in your dashboard and via the chat assistant.
- **Professional UI/UX:** A sleek, Bootstrap-inspired dark mode frontend with micro-animations and a responsive design.
- **Complete User Flow:** Includes user authentication, cart management, and a fully interactive mock payment gateway.

## 🏗️ Architecture

- **Backend:** FastAPI (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **AI Integration:** OpenAI API (`gpt-4o` / `gpt-3.5-turbo`) utilizing native Tool Calling for seamless database querying.
- **Frontend:** HTML, Vanilla CSS, and JavaScript (Jinja2 Templates).
- **Data Pipeline:** Custom Python script to synthetically generate realistic mock products scaling to hundreds of items.

## 🛠️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/EshanDasarwarProdapt/AI_Shopping_Chat_BOT.git
   cd AI_Shopping_Chat_BOT
   ```

2. **Install dependencies**
   Ensure you have Python 3.8+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.env` file in the root directory and add your OpenAI API Key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Seed the Database**
   Initialize the SQLite database and seed it with all 250 products:
   ```bash
   python reset_db.py
   ```

5. **Run the Server**
   Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the Application**
   Open your browser and navigate to `http://localhost:8000`.

## 💡 How it Works (AI Flow)

1. **Understand Intent:** The AI parses the user's message to detect intent (search, compare, ask spec, recommend).
2. **Fetch Data:** It triggers Python functions (`search_catalog`, `get_recommendations`, etc.) to query the SQLite product database.
3. **Ground Response:** The fetched data is injected into the LLM prompt so it never hallucinates prices or specifications.
4. **Personalize:** The `get_recommendations` tool factors in the logged-in user's recent browsing and purchase history to provide highly personalized suggestions.
