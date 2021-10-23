from pydantic import BaseModel, Field
from typing import Optional


class AuthDetails(BaseModel):
    username: str
    password: str


class Project(BaseModel):
    projectname: Optional[str] = Field(None, title="The name of the project", max_length=30)
    description: Optional[str] = Field(None, title="The description of the project", max_length=100)