import logging
import os
from auth_gateway import config
from auth_gateway.services import authentication, authorization
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    token: str

@app.post("/login")
async def login(user: User):
    try:
        token = authentication.authenticate_user(user.username, user.password)
        return JSONResponse(content={"token": token}, status_code=200)
    except Exception as e:
        logging.error(f"Error logging in user: {e}")
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/protected")
async def protected(token: str):
    try:
        if authorization.authorize_token(token):
            return JSONResponse(content={"message": "Hello, authenticated user!"}, status_code=200)
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logging.error(f"Error authorizing token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))