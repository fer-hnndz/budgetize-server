"""Data Models for Fastapi Request"""

from pydantic import BaseModel


class TokenBody(BaseModel):
    token: str


class SetupBody(BaseModel):
    token_id: str
    main_currency: str
    timezone: str


class AccountCreate(BaseModel):
    user_token: str
    name: str
    currency: str
    icon: str
    initial_balance: float
