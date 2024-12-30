from fastapi import APIRouter
from sqlmodel import Session, select

from budgetize_server.database import engine, models

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
async def get_all_users():
    with Session(engine) as session:
        return session.exec(select(models.User)).all()
