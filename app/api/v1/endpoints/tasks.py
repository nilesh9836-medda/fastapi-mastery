from fastapi import APIRouter, Depends, status
from app.schemas.task import TaskCreate, TaskResponse
from app.api.deps import load_tasks, save_tasks, get_task_or_404, pagination_params

router = APIRouter()
    
# --- LIST ---
@router.get("/", response_model=list[TaskResponse])
async def list_tasks(pagination: dict = Depends(pagination_params)):
    tasks = load_tasks()
    return tasks[pagination["skip"] : (pagination["skip"] + pagination["limit"])]

# --- GET ONE ---
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task: dict = Depends(get_task_or_404)):
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
async def update_task(task_id: int, updated: TaskCreate, existing_task: dict = Depends(get_task_or_404)):
    tasks = load_tasks()
    for task in tasks:
        if task_id == task["title"]:     
            task["title"] = updated.title
            task["description"] = updated.description
            task["is_done"] = updated.is_done
    save_tasks(tasks)
    return existing_task["title": updated.title, "description": updated.description, "is_done":  updated.is_done]

# --- DELETE ---
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task: dict = Depends(get_task_or_404)):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task["id"]]
    save_tasks(tasks)
    return None # 204 means no body