from fastapi import FastAPI
from api.routes.submit import router as submit_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(submit_router)