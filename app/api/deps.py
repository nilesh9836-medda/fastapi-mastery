import json
from pathlib import Path
from fastapi import HTTPException

DB_FILE = Path("app/db/tasks.json")

def load_tasks () -> list[dict]:
    if not DB_FILE.exists():
        return DB_FILE.write_text("[]")
    try:
        return json.loads(DB_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    
def save_tasks(tasks: list[dict]):
    DB_FILE.write_text(json.dumps(tasks, indent=2, default= str), encoding = "utf-8")
    

#--------------- This is a dependency ------------------------
def get_task_or_404(task_id: int) -> dict:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code= 404, detail=f"Task {task_id} not found")

#----------------Another dependency -> Pagination ------------------
def pagination_params(skip: int = 0, limit: int = 10):
    if limit > 100: limit = 100
    return {"skip": skip, "limit": limit}
