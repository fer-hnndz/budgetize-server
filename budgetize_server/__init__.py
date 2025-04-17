"""Budgetize's server module"""

import arrow
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager


# Routers
from .routers import currency

scheduler = BackgroundScheduler()


def scheduled_transaction_job():
    now = arrow.Arrow.now()
    print(f"Scheduled job running at {now.format('YYYY-MM-DD HH:mm:ss')}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for the FastAPI app."""

    # Start the scheduler
    scheduler.add_job(scheduled_transaction_job, "interval", seconds=10)
    scheduler.start()
    yield
    # Shutdown the scheduler
    scheduler.shutdown()


app = FastAPI(
    title="Budgetize",
    description="The open source finance app for budgeting and tracking expenses.",
    summary="Budgetize API",
    version="0.1.0",
    lifespan=lifespan,
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
