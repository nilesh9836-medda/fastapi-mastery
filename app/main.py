from fastapi import FastAPI
from app.api.v1.api import api_router

app = FastAPI(title="Task Manager API")

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")     # -> http://127.0.0.1:8000/hello/Riya
async def health_check():
    return {"status": "ok"}
