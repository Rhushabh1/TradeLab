from pydantic import BaseModel, EmailStr


# schema of auth requests (used in auth API)
class RegisterRequest(BaseModel):
	email : EmailStr
	password : str 

class LoginRequest(BaseModel):
	email : EmailStr
	password : str 

class TokenResponse(BaseModel):
	access_token : str 
	token_type : str = "bearer"