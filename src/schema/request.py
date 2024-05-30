import re
from pydantic import BaseModel, EmailStr, validator
from fastapi import HTTPException


class SignUpRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator('username', 'email', 'password')
    def valid_empty(cls, v):
        if not v or v == "":
            raise HTTPException(status_code=422, detail="Enter The Required Fields")
        return v
    
    @validator('password')
    def valid_password(cls, v):
        if len(v) < 8:
            raise HTTPException(status_code=422, detail="At Least 8")
        
        if not re.search(r"[a-z]", v):
            raise HTTPException(status_code=422, detail="At Least 1 Lowercase Letter")
        
        if not re.search(r"[A-Z]", v):
            raise HTTPException(status_code=422, detail="At Least 1 Uppercase Letter")
        
        if not re.search(r"[!@#$%^&*()]", v):
            raise HTTPException(status_code=422, detail="At Least 1 Special Character")

        return v