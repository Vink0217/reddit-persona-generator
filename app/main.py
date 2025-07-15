from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from pathlib import Path
import os
import re
from dotenv import load_dotenv
from datetime import datetime
from Summary import fetch_and_store_user_data, generate_persona

load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = "reddit_persona"
COLLECTION_NAME = "users"

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def check_persona_exists(username: str) -> bool:
    """Check if a complete persona already exists in MongoDB"""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    data = db[COLLECTION_NAME].find_one({"username": username})
    client.close()
    
    if not data:
        return False
    
    # Check if persona analysis fields exist (indicating LLM analysis was completed)
    required_fields = ["name", "age", "occupation", "personality", "feelings"]
    return all(field in data for field in required_fields)

@app.get("/")
async def show_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def handle_submission(request: Request, reddit_url: str = Form(...)):
    # Multiple regex patterns to handle different Reddit URL formats
    patterns = [
        r"/u/([A-Za-z0-9_-]+)",           # /u/username
        r"/user/([A-Za-z0-9_-]+)",        # /user/username
        r"reddit\.com/u/([A-Za-z0-9_-]+)", # reddit.com/u/username
        r"reddit\.com/user/([A-Za-z0-9_-]+)", # reddit.com/user/username
        r"^([A-Za-z0-9_-]+)$"             # Just username
    ]
    
    username = None
    for pattern in patterns:
        match = re.search(pattern, reddit_url)
        if match:
            username = match.group(1)
            break
    
    if not username:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "❌ Invalid Reddit URL. Use https://reddit.com/u/username or just enter the username"
        })

    try:
        print(f"🔄 Processing persona for: {username}")
        
        # Check if persona already exists
        if check_persona_exists(username):
            print(f"✅ Persona for {username} already exists in database, skipping analysis")
        else:
            print(f"🔄 Running fresh persona analysis for: {username}")
            
            # Fetch user data and store in MongoDB
            fetch_and_store_user_data(username)
            
            # Generate persona analysis
            generate_persona(username)
        
        # Retrieve the persona from MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        data = db[COLLECTION_NAME].find_one({"username": username})
        client.close()
        
        if data:
            return templates.TemplateResponse("combined.html", {
                "request": request,
                "persona": data,
                "username": username,
                "success": True
            })
        else:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "error": f"⚠️ Failed to generate persona for '{username}'"
            })
            
    except Exception as e:
        print(f"❌ Error processing {username}: {str(e)}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"❌ Error processing user: {str(e)}"
        })

@app.get("/persona")
async def view_persona(request: Request, user: str):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    data = db[COLLECTION_NAME].find_one({"username": user})
    client.close()

    if data:
        return templates.TemplateResponse("combined.html", {
            "request": request,
            "persona": data,
            "username": user,
            "success": True
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "error": f"⚠️ No persona found for '{user}'"
    })

@app.post("/refresh")
async def refresh_persona(request: Request, reddit_url: str = Form(...)):
    """Force refresh a persona even if it exists"""
    # Same URL parsing logic as main handler
    patterns = [
        r"/u/([A-Za-z0-9_-]+)",
        r"/user/([A-Za-z0-9_-]+)",
        r"reddit\.com/u/([A-Za-z0-9_-]+)",
        r"reddit\.com/user/([A-Za-z0-9_-]+)",
        r"^([A-Za-z0-9_-]+)$"
    ]
    
    username = None
    for pattern in patterns:
        match = re.search(pattern, reddit_url)
        if match:
            username = match.group(1)
            break
    
    if not username:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "❌ Invalid Reddit URL"
        })

    try:
        print(f"🔄 Force refreshing persona for: {username}")
        
        # Always fetch fresh data and regenerate persona
        fetch_and_store_user_data(username)
        generate_persona(username)
        
        # Retrieve the updated persona
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        data = db[COLLECTION_NAME].find_one({"username": username})
        client.close()
        
        if data:
            return templates.TemplateResponse("combined.html", {
                "request": request,
                "persona": data,
                "username": username,
                "success": True
            })
        else:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "error": f"⚠️ Failed to refresh persona for '{username}'"
            })
            
    except Exception as e:
        print(f"❌ Error refreshing {username}: {str(e)}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"❌ Error refreshing user: {str(e)}"
        })