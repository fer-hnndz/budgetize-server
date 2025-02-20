from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

# Routers
from .routers import currency

app = FastAPI(
    title="Budgetize",
    description="The open source finance app for budgeting and tracking expenses.",
    summary="Budgetize API",
    version="0.1.0",
)


app.include_router(currency.router)

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
