from fastapi import FastAPI

app = FastAPI(title="Task Manager API - Chapter 1")

@app.get("/")       # -> http://127.0.0.1:8000/
async def root():
    return {"message": "API is running"}

@app.get("/hello/{name}")       # -> http://127.0.0.1:8000/hello/Riya
async def hello(name: str):
    return {"messege": f"Hello, {name}"}

@app.get("/health")     # -> http://127.0.0.1:8000/hello/Riya
async def health_check():
    return {"status": "ok"}
