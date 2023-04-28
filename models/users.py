from pydantic import BaseModel, EmailStr
from typing import List, Optional

from models.events import Event


class User(BaseModel):
    email: EmailStr
    password: str
    events: Optional[List[Event]]

    class Config:
        schema_extra = { 
            "example": {
            "email": "fastapi@packt.com",
            "username": "strong!!!", 
            "events": [],
        }
    }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        frozen = True
        schema_extra = { 
            "example": {
            "email": "fastapi@packt.com",
            "password": "strong!!!", 
            "events": [],
            }
        }
