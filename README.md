# 🤖 AI Task Manager Agent

מערכת חכמה לניהול משימות המבוססת על סוכן בינה מלאכותית (AI Agent). 
המערכת מאפשרת למשתמש לנהל את המשימות שלו דרך שיחה חופשית בעברית, תוך שימוש במודל השפה Llama 3.3.

## 🌟 יכולות המערכת
* **שיחה טבעית:** הוספה, צפייה וניהול משימות באמצעות טקסט חופשי.
* **ביצוע פעולות (Tool Calling):** הסוכן יודע מתי להפעיל פונקציות פייתון כדי לעדכן את רשימת המשימות.
* **ממשק משתמש מודרני:** UI שנבנה ב-React עם עיצוב נקי וחווית משתמש חלקה.
* **Backend מהיר:** שרת FastAPI המנהל את התקשורת בין המודל לממשק.

## 🛠 טכנולוגיות
* **Frontend:** React 19, Vite, Custom CSS3 Styling.
* **Backend:** Python, FastAPI, Uvicorn.
* **AI Model:** Llama 3.3-70b (via Groq Cloud).
* **Core Logic:** Function Calling architecture for task management.

## 🚀 איך מפעילים את הפרויקט?

### 1. דרישות קדם
* Python 3.10 ומעלה.
* Node.js מותקן.
* מפתח API מ-Groq Cloud.

### 2. הגדרת השרת (Backend)
```bash
# התקנת ספריות (יש לוודא קיום requirements.txt)
pip install fastapi uvicorn groq python-dotenv

# יצירת קובץ .env והוספת המפתח
echo "GROQ_API_KEY=your_key_here" > .env

# הרצת השרת
uvicorn main:app --reload