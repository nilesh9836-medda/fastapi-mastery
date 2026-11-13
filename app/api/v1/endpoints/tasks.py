import json
from pathlib import Path
from fastapi import APIRouter
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter()

DB_FILE =  Path("app/db/tasks.json")

def load_tasks() -> list[dict]:
    if not DB_FILE.exists():
        return DB_FILE.write_text("[]")
    try:
        return json.loads(DB_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("tasks.json corrupted, starting fresh")
        return []
    
def save_tasks(tasks: list[dict]):
    DB_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
    
@router.get("/", response_model=list[TaskResponse])
async def list_tasks(is_done: bool | None = None, search: str | None = None):
    tasks = load_tasks()
    results = tasks
    if is_done is not None:
        results = [t for t in results if t["is_done"] == is_done]
    if search:
        results = [t for t in results if search.lower() in t["title"].lower]
    return results

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            return task
    return {"id": task_id, "title": "Not found", "description": None, "is_done": False}

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate):
    tasks = load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {
        "id": new_id,
        "title": task.title,
        "description": task.description,
        "is_done": task.is_done
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task