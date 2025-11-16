from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routers
from routers.chat_stream import chat_stream_router
from routers.site import site_router   # 如果你有這個
# from routers.xxx import xxx_router

app = FastAPI()

# CORS（你可以加上前端 domain）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat_stream_router)
app.include_router(site_router)  # 如果有


@app.get("/")
def root():
    return {"status": "ok", "service": "red-backend"}