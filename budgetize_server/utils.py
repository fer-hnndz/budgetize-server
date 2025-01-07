import os
from typing import Optional

from fastapi import HTTPException, status
from google.auth.transport import requests
from google.oauth2 import id_token
from sqlmodel import Session, select

from budgetize_server.database import models


def _verify_google_token(token: str) -> Optional[models.UserBase]:
    """
    Verifies that the Google OAuth Token is valid and retrieves the user's information.

    Args:
        token (str): The Google OAuth Token.
    """

    try:
        CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
        user_info = id_token.verify_oauth2_token(
            token, requests.Request(), CLIENT_ID, clock_skew_in_seconds=60
        )

        return models.UserBase(
            email=user_info["email"],
            name=user_info["name"],
            provider_id=user_info["sub"],
            picture_url=user_info.get("picture"),
        )
    except Exception as e:
        print(e)
        return None


async def get_user_from_token(token: str, engine) -> models.User:
    """
    (Coroutine) Retrieves the user from the token.
    Creates it if it doesn't exist.

    Args:
        token (str): The Google OAuth Token
    """

    user = _verify_google_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    with Session(engine) as session:
        db_user = session.exec(
            select(models.User).where(models.User.email == user.email)
        ).first()

        if not db_user:
            db_user = models.User(
                email=user.email,
                name=user.name,
                picture_url=user.picture_url,
            )
            session.add(db_user)
            session.commit()

        return db_user
