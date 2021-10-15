from pydantic import BaseModel, Field
from typing import Optional

class AuthDetails(BaseModel):
    username: str
    password: str

class Project(BaseModel):
    method : str
    name: str
    description: Optional[str] = Field(None, title="The description of the item", max_length=100)



