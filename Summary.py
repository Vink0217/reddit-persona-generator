import os
import json
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
import praw
import google.generativeai as genai

# --- ENV SETUP ---
load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = "reddit_persona"
COLLECTION_NAME = "users"

# --- INIT GEMINI ---
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("FATAL: GEMINI_API_KEY not set.")
    exit()

# --- INIT REDDIT ---
def get_reddit_instance():
    return praw.Reddit(
        client_id=os.environ.get("REDDIT_CLIENT_ID"),
        client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
        user_agent=os.environ.get("REDDIT_USER_AGENT"),
    )

# --- FETCH USER DATA FROM REDDIT AND STORE ---
def fetch_and_store_user_data(username: str):
    reddit = get_reddit_instance()
    redditor = reddit.redditor(username)
    posts = list(redditor.submissions.new(limit=100))
    comments = list(redditor.comments.new(limit=100))

    user_data = {
        "username": redditor.name,
        "account_created_utc": redditor.created_utc,
        "comment_karma": redditor.comment_karma,
        "link_karma": redditor.link_karma,
        "has_verified_email": redditor.has_verified_email,
        "posts": [
            {
                "id": p.id,
                "title": p.title,
                "selftext": p.selftext,
                "subreddit": p.subreddit.display_name,
                "created_utc": p.created_utc,
                "url": p.url,
                "is_self": p.is_self,
                "is_video": p.is_video,
                "score": p.score,
                "upvote_ratio": getattr(p, "upvote_ratio", None),
                "link_flair_text": getattr(p, "link_flair_text", None),
            }
            for p in posts
        ],
        "comments": [
            {
                "id": c.id,
                "body": c.body,
                "subreddit": c.subreddit.display_name,
                "created_utc": c.created_utc,
                "score": c.score,
                "author_flair_text": getattr(c, "author_flair_text", None),
            }
            for c in comments
        ],
    }

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    collection.update_one({"username": username}, {"$set": user_data}, upsert=True)
    client.close()
    print("✅ User data stored in MongoDB.")
    return user_data

# --- RETRIEVE USER DATA ---
def get_user_data(username: str):
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        data = collection.find_one({"username": username})
        client.close()
        return data
    except Exception as e:
        print(f"❌ Error accessing DB: {e}")
        return None

# --- FIND QUOTE SOURCE ---
def find_source_of_quote(quote, user_data):
    for post in user_data.get("posts", []):
        if quote in post.get("title", "") or quote in post.get("selftext", ""):
            return {
                "type": "post",
                "id": post.get("id"),
                "subreddit": post.get("subreddit"),
                "text": post.get("selftext", "") or post.get("title", "")
            }
    for comment in user_data.get("comments", []):
        if quote in comment.get("body", ""):
            return {
                "type": "comment",
                "id": comment.get("id"),
                "subreddit": comment.get("subreddit"),
                "text": comment.get("body")
            }
    return None

# --- LLM ANALYSIS ---
def analyze_with_llm(user_data):
    print("🤖 Calling Gemini for analysis...")
    text_corpus = ""
    for post in user_data.get("posts", []):
        text_corpus += f"Post Title: {post.get('title', '')}\nPost Body: {post.get('selftext', '')}\n---\n"
    for comment in user_data.get("comments", []):
        text_corpus += f"Comment: {comment.get('body', '')}\n---\n"

    json_format_definition = """{
        "name": {"value": "string", "justification": "string", "citations": ["exact quote from text"]},
        "age": {"value": "string", "justification": "string", "citations": ["exact quote from text"]},
        "occupation": {"value": "string", "justification": "string", "citations": ["exact quote from text"]},
        "status": {"value": "string", "justification": "string", "citations": ["exact quote from text"]},
        "location": {"value": "string", "justification": "string", "citations": ["exact quote from text"]},
        "tier": {"value": "string", "justification": "string", "citations": ["exact quote from text"]},
        "archetype": {"value": "string", "justification": "string", "citations": ["exact quote from text"]},
        "behaviour_and_habits": {"value": ["habit1", "habit2"], "justification": "string", "citations": ["exact quote from text"]},
        "frustrations": {"value": ["frustration1", "frustration2"], "justification": "string", "citations": ["exact quote from text"]},
        "motivations": {"value": ["motivation1", "motivation2"], "justification": "string", "citations": ["exact quote from text"]},
        "personality": {"value": ["trait1", "trait2"], "justification": "string", "citations": ["exact quote from text"]},
        "goals_and_needs": {"value": ["goal1", "need1"], "justification": "string", "citations": ["exact quote from text"]},
        "feelings": {
            "happiness": {"score": 0, "justification": "string", "citations": ["exact quote from text"]},
            "anger": {"score": 0, "justification": "string", "citations": ["exact quote from text"]},
            "anxiety": {"score": 0, "justification": "string", "citations": ["exact quote from text"]},
            "sadness": {"score": 0, "justification": "string", "citations": ["exact quote from text"]},
            "confidence": {"score": 0, "justification": "string", "citations": ["exact quote from text"]}
        }
    }"""

    prompt = f"""
You are an expert persona analyst. Analyze the Reddit user's text to fill out this JSON structure with strict evidence-based inference.

For the "feelings" field, infer a score from 0 (not present) to 100 (very strong) for each feeling (happiness, anger, anxiety, sadness, confidence), with a justification and direct citations from the text.

TEXT CORPUS:
---
{text_corpus}
---

REQUIRED OUTPUT FORMAT:
{json_format_definition}
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        cleaned = response.text.strip().replace("```json\n", "").replace("\n```", "")
        return json.loads(cleaned)
    except Exception as e:
        print("❌ LLM Error:", e)
        return None

# --- FINAL PERSONA CREATION ---
def generate_persona(username):
    # Load user_data from MongoDB
    client = MongoClient(MONGO_URI)
    db = client["reddit_persona"]
    collection = db["users"]

    user_data = collection.find_one({"username": username})
    if not user_data:
        print(f"❌ No user data found for {username}. Please run fetch step first.")
        return

    # Basic metadata
    persona = {
        "username": user_data.get("username", username),
        "link_karma": user_data.get("link_karma", 0),
        "comment_karma": user_data.get("comment_karma", 0),
        "account_age_days": (datetime.now() - datetime.fromtimestamp(user_data.get("account_created_utc", 0))).days,
    }

    # Call LLM to get persona analysis
    print("🔍 Analyzing persona via LLM...")
    llm_result = analyze_with_llm(user_data)

    if not llm_result:
        print("⚠️ LLM returned no data.")
        return

    # Merge LLM results into the base persona
    persona.update(llm_result)

    # Optional: Attach citations' original source text
    for key, obj in persona.items():
        if isinstance(obj, dict) and "citations" in obj:
            obj["citations"] = [
                find_source_of_quote(quote, user_data)
                for quote in obj.get("citations", [])
            ]

    # Save merged persona back to MongoDB
    collection.update_one({"username": username}, {"$set": persona}, upsert=True)
    client.close()

    # Save to file too (optional)
    '''
    with open(f"{username}_persona_analysis.json", "w", encoding="utf-8") as f:
        import json
        json.dump(persona, f, indent=2, ensure_ascii=False)

    print(f"✅ Persona for {username} saved to MongoDB and {username}_persona_analysis.json")
    '''


# --- MAIN EXEC ---
if __name__ == "__main__":
    uname = input("🔍 Enter Reddit username to analyze: ").strip()
    fetch_and_store_user_data(uname)
    generate_persona(uname)