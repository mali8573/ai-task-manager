# tools_config.py

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "הוספת משימה חדשה למערכת עם פרטים מלאים",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "כותרת המשימה"},
                    "description": {"type": "string", "description": "תיאור מפורט של המשימה"},
                    "task_type": {"type": "string", "description": "סוג המשימה (למשל: עבודה, אישי, לימודים)"},
                    "start_date": {"type": "string", "description": "תאריך תחילת המשימה"},
                    "end_date": {"type": "string", "description": "תאריך סיום המשימה"},
                    "status": {"type": "string", "description": "סטטוס המשימה (ברירת מחדל: פתוח)"}
                },
                "required": ["title"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "שליפת רשימת משימות עם אפשרות לסינון",
            "parameters": {
                "type": "object",
                "properties": {
                    "filter_status": {"type": "string", "description": "סינון לפי סטטוס המשימה"},
                    "filter_type": {"type": "string", "description": "סינון לפי סוג המשימה"}
                },
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "עדכון פרטי משימה קיימת לפי מזהה (ID)",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "המזהה הייחודי של המשימה"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "status": {"type": "string"},
                    "end_date": {"type": "string"}
                },
                "required": ["task_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "מחיקת משימה מהמערכת לפי מזהה (ID)",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "מזהה המשימה למחיקה"}
                },
                "required": ["task_id"],
                "additionalProperties": False
            }
        }
    }
]