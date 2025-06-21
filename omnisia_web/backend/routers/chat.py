from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    text: str


@router.post("/")
async def chat(req: ChatRequest):
    # Simple echo placeholder
    return {"response": f"You said: {req.text}"}
