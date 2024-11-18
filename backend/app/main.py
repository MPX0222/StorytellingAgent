from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import game_controller, dialogue_controller

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(game_controller.router, prefix="/api/game", tags=["game"])
app.include_router(dialogue_controller.router, prefix="/api/dialogue", tags=["dialogue"])

@app.get("/")
async def root():
    return {"message": "Story Agent Game API"}