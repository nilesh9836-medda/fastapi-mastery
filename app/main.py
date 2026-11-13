from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router

app = FastAPI(title="Task Manager API")

# Allow any frontend to call this API (for learning, allow all)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # in production, put your real domain here
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")     # -> http://127.0.0.1:8000/health
async def health_check():
    return {"status": "ok"}
