from pydantic import BaseModel


class TokenBody(BaseModel):
    token: str
