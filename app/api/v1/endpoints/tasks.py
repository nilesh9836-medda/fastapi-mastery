import json
from pathlib import Path
from fastapi import APIRouter, HTTPException, status
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
    
def find_task(tasks: list[dict], task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None
    
# --- LIST ---
@router.get("/", response_model=list[TaskResponse])
async def list_tasks(is_done: bool | None = None, search: str | None = None):
    tasks = load_tasks()
    if is_done is not None:
        tasks = [t for t in tasks if t["is_done"] == is_done]
    if search:
        tasks = [t for t in tasks if search.lower() in t["title"].lower]
    return tasks

# --- GET ONE ---
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task

# --- CREATE ---
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
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

# --- UPDATE (PUT) ---
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, updated: TaskResponse):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    # PUT = replace whole task
    task["title"] = updated.title
    task["description"] = updated.description
    task["is_done"] = updated.is_done
    save_tasks(tasks)
    return task

# --- DELETE ---
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    tasks.remove(task)
    save_tasks(tasks)
    return None # 204 means no body