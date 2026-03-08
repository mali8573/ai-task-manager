import os
import json
import re
from groq import Groq
from todo_service import add_task, get_tasks, update_task, delete_task
from tools_config import tools
from dotenv import load_dotenv

load_dotenv()

# הגדרת הלקוח
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def run_agent(query, chat_history=[]):
    """
    מנהל את השיחה עם המודל, מפעיל פונקציות ומחזיר תגובה אנושית.
    """
    system_instruction = {
        "role": "system",
        "content": """אתה עוזר אישי מקצועי לניהול משימות. 
        חוקים נוקשים:
        1. ענה תמיד בעברית ברורה, טבעית ומנומסת.
        2. אל תציג למשתמש קוד, סוגריים מסולסלים {}, או פורמט JSON בשום פנים ואופן.
        3. אם פונקציה מחזירה נתונים טכניים, תרגם אותם למשפט אנושי.
        4.   הסתמך אך ורק על המידע שמתקבל מהכלים (Tools) ואל תמציא משימות שלא קיימות.
        5. אם המשתמש מבקש פרטים, הצג אותם ברשימה נקייה ומסודרת."""
    } 

    messages = [system_instruction] + chat_history + [{"role": "user", "content": query}]

    # קריאה ראשונה למודל
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    
    # בדיקה האם המודל ביקש להפעיל כלים
    if response_message.tool_calls:
        messages.append(response_message)
        
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            
            # ניקוי וטעינת הארגומנטים
            args_raw = tool_call.function.arguments
            try:
                json_match = re.search(r'\{.*\}', args_raw, re.DOTALL)
                args = json.loads(json_match.group()) if json_match else json.loads(args_raw)
            except:
                args = {}

            # הגנה: וודא שהארגומנטים הם מילון
            if args is None:
                args = {}

            # מיפוי והפעלת הפונקציה
            if function_name == "add_task":
                result = add_task(**args)
            elif function_name == "get_tasks":
                result = get_tasks(**args) 
            elif function_name == "update_task":
                result = update_task(**args)
            elif function_name == "delete_task":
                result = delete_task(**args)
            else:
                result = {"error": "הפונקציה לא קיימת"}

            # הוספת תוצאת הפונקציה להיסטוריה (בתוך הלולאה!)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": json.dumps(result, ensure_ascii=False)
            })

        # קריאה שנייה למודל - מחוץ ללולאת ה-for אבל בתוך ה-if
        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return final_response.choices[0].message.content, messages[1:]

    # אם לא הופעלו כלים
    return response_message.content, messages[1:]