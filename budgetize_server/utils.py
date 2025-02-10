from fastapi import HTTPException, status

from budgetize_server.database import models


async def get_user_from_token(token: str, engine) -> models.User:
    """
    (Coroutine) Retrieves the user from the token.
    Creates it if it doesn't exist.

    Args:
        token (str): The Google OAuth Token
    """

    return None
