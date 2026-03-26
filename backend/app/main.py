from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_tables
from app.routes.auth import router as auth_router
from app.routes.groups import router as groups_router
from app.routes.expenses import router as expenses_router
from app.routes.balances import router as balances_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(title="SplitTrail", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(groups_router)
app.include_router(expenses_router)
app.include_router(balances_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": "SplitTrail"}