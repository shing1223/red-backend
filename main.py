from fastapi import FastAPI
from api.routes.submit import router as submit_router
from api.routes.chat_stream import router as chat_stream_router
app.include_router(chat_stream_router)

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(submit_router)