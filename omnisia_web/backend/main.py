from fastapi import FastAPI
from .routers import upload, preprocess, train, chat

app = FastAPI(title="OmnisIA Trainer Web")

app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(preprocess.router, prefix="/preprocess", tags=["preprocess"])
app.include_router(train.router, prefix="/train", tags=["train"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])


@app.get("/")
async def root():
    return {"message": "OmnisIA Trainer Web API"}
