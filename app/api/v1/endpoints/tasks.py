from fastapi import APIRouter
from app.schemas.task import TaskCreate, TaskResponse
#from typing import Annotated

router = APIRouter()

fake_db = []
fake_id_counter = 1

@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    is_done: bool | None = None,
    #search: Annotated[str | None, Query(max_length=50)] = None
):
    results = fake_db
    if is_done is not None:
        results = [t for t in results if t["is_done"] == is_done]
   #if search:
    #    results = [t for t in results if search.lower() in t["title"].lower()]
    return results

@router.get("/{task_id}", response_model=TaskResponse)
async def create_task(task_id: int):
    for task in fake_db:
        if task["id"] == task_id:
            return task
    return {"id": task_id, "title": "Not found"}

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate):
    global fake_id_counter
    new_task = {
        "id": fake_id_counter,
        "title": task.title,
        "description": task.description,
        "is_done": task.is_done
    }
    fake_db.append(new_task)
    fake_id_counter += 1
    return new_task