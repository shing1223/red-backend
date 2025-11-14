from fastapi import FastAPI
from api.routes.submit import router as submit_router

app = FastAPI()

app.include_router(submit_router)