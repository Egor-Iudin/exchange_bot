from pydantic import BaseModel, Field
from typing import List


class User(BaseModel):
    telegram_id: int = Field(...)
    stocks: List[int] = Field(...)
