"""Data Models for Fastapi Request"""

from pydantic import BaseModel


class TokenBody(BaseModel):
    token: str


class SetupBody(BaseModel):
    token_id: str
    main_currency: str
    timezone: str
