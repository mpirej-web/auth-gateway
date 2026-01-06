import logging
import os
from auth_gateway import settings
from auth_gateway.auth import Authenticator
from auth_gateway.models import User
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional

# Initialize logging
logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

app = FastAPI()

# Define OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def get_user(username: str):
    user = User.get_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user.check_password(password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = Authenticator.decode_token(token)
        token_data = TokenData(**payload)
        user = get_user(token_data.username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    access_token = Authenticator.encode_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user