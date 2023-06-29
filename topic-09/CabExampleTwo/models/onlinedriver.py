from typing import Optional
from sqlmodel import Field, SQLModel


class OnlineDriver(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    latitude: float
    longitude: float
