from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    is_done: bool = False
    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    is_done: bool = False
    
    class Config:
        from_attribute = True