from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from budgetize_server.database import engine

# Routers
from .routers import currency, user

SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="Budgetize",
    description="The open source finance app for budgeting and tracking expenses.",
    summary="Budgetize API",
    version="0.1.0",
)


app.include_router(currency.router)
app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)


@app.get("/")
async def index():
    return {"message": "Hello, World!", "status": 200}
