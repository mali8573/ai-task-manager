# todo_service.py

# מערך גלובלי שישמש כמסד הנתונים שלנו (כפי שהוגדר בדרישות כ"הנחה")
tasks_db = []
id_counter = 1

def add_task(title, description=None, task_type=None, start_date=None, end_date=None, status="פתוח"):
    """
    הוספת משימה חדשה עם כל המאפיינים הנדרשים:
    קוד, כותרת, תיאור, סוג, תאריך התחלה, תאריך סיום וסטטוס.
    """
    global id_counter
    
    new_task = {
        "id": id_counter,
        "title": title,
        "description": description,
        "type": task_type,
        "start_date": start_date,
        "end_date": end_date,
        "status": status
    }
    
    tasks_db.append(new_task)
    id_counter += 1
    return new_task

def get_tasks(filter_status=None, filter_type=None):
    # אם אין משימות, נחזיר רשימה ריקה בצורה מפורשת
    if not tasks_db:
        return []
    
    filtered_tasks = tasks_db
    if filter_status:
        filtered_tasks = [t for t in filtered_tasks if t["status"] == filter_status]
    if filter_type:
        filtered_tasks = [t for t in filtered_tasks if t["type"] == filter_type]
        
    return filtered_tasks
def update_task(task_id, **updates):
    """
    עדכון משימה קיימת. הוספנו המרה ל-int כדי למנוע אי-התאמה של סוגי נתונים.
    """
    try:
        # המרה ל-int למקרה שהמודל שלח מחרוזת "1" במקום מספר 1
        target_id = int(task_id)
    except (ValueError, TypeError):
        return {"error": "מזהה משימה לא תקין"}

    for task in tasks_db:
        if task["id"] == target_id:
            task.update(updates)
            return task
    return {"error": "משימה לא נמצאה"}
def delete_task(task_id):
    global tasks_db
    try:
        # המרה ל-int ליתר ביטחון
        target_id = int(task_id)
    except:
        return {"status": "error", "message": "מזהה לא תקין"}

    initial_length = len(tasks_db)
    tasks_db = [t for t in tasks_db if t["id"] != target_id]
    
    if len(tasks_db) < initial_length:
        return {"status": "success", "message": f"משימה {target_id} נמחקה"}
    return {"status": "error", "message": "משימה לא נמצאה"}