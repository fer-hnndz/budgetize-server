import os
from typing import Optional

from google.auth.transport import requests
from google.oauth2 import id_token

from budgetize_server.database.models import UserBase


def verify_google_token(token: str) -> Optional[UserBase]:
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

        return UserBase(
            email=user_info["email"],
            name=user_info["name"],
            provider_id=user_info["sub"],
            picture_url=user_info.get("picture"),
        )
    except Exception as e:
        print(e)
        return None
