from typing import Optional
from sqlmodel import Field, SQLModel


class Driver(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    license_number: str
    address: str
    mobile_number: str
    username: str
    password: str
    taxi_number: int
