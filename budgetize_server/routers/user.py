from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from budgetize_server.data_models import TokenBody
from budgetize_server.database import engine, models
from budgetize_server.utils import verify_google_token

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/auth")
async def auth_user(data: TokenBody):
    """Allows User to authenticate themselves."""

    print("recieved token: ", data)
    user_data = verify_google_token(data.token)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    with Session(engine) as session:
        user = session.exec(
            select(models.User).where(models.User.email == user_data.email)
        ).first()

        if not user:
            user = models.User(
                email=user_data.email,
                name=user_data.name,
                picture_url=user_data.picture_url,
            )
            session.add(user)
            session.commit()

    return {
        "name": user_data.name,
        "email": user_data.email,
        "picture_url": user_data.picture_url,
    }
