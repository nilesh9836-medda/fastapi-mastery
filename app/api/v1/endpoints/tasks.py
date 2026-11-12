from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_tasks():
    return [{"id": 1, "title": "Learn FastAPI"}]

@router.get("/{task_id}")
async def get_task(task_id: int):
    return {"id": task_id, "title": f"Task {task_id}"}