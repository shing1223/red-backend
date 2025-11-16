from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.chat_stream import chat_stream_router
from api.routes.submit import site_router
from routers.search import router as search_router
from routers.site import router as site_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat_stream_router)
app.include_router(site_router)
app.include_router(search_router)

@app.get("/")
def root():
    return {"status": "ok", "service": "red-backend"}