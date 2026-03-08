import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# ייבוא פונקציית הרצת הסוכן מהקובץ שלך
from agent_service import run_agent

# טעינת מפתח ה-API מהקובץ .env
load_dotenv()

app = FastAPI(title="Task Management Agent API")

# הגדרות CORS - מאפשר ל-React לתקשר עם השרת בקלות
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# מסד נתונים זמני בזיכרון לשמירת היסטוריית השיחה
sessions_db = {}

# --- חיבור ה-Frontend (קבצי ה-React שנמצאים ב-static) ---

# חיבור תיקיית ה-assets (CSS, JS) כדי שהעיצוב ייטען
assets_path = os.path.join("static", "assets")
if os.path.exists(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="static_assets")

@app.get("/")
async def serve_ui():
    """מציג את אפליקציית הריאקט כדף הבית"""
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "קובץ index.html לא נמצא בתיקיית static. ודאי שהעברת את תוצרי ה-build."}

# --- הגדרות ה-API של הצ'אט ---

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """נקודת הקצה שמקבלת הודעה ומחזירה תשובה מהסוכן"""
    try:
        # שליפת היסטוריית השיחה (או רשימה ריקה אם זו שיחה חדשה)
        history = sessions_db.get(request.user_id, [])
        
        # הרצת הסוכן (קריאה ל-agent_service.py)
        answer, updated_history = run_agent(request.message, history)
        
        # שמירת 10 ההודעות האחרונות בזיכרון
        sessions_db[request.user_id] = updated_history[-10:]
        
        return ChatResponse(response=answer)
        
    except Exception as e:
        print(f"Server Error: {e}")
        return ChatResponse(response="סליחה, נתקלתי בבעיה קלה בעיבוד הבקשה. נסי שוב בעוד רגע.")

@app.get("/health")
async def health_check():
    """בדיקה שהשרת באוויר"""
    return {"status": "online"}

# טיפול בנתיבים של React Router - שולח את כל שאר הבקשות ל-index.html
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404)