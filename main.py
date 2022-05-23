from fastapi import FastAPI, status, Depends
from fastapi_login import LoginManager
from fastapi.middleware.cors import CORSMiddleware
from db import database, users
from pydantic import BaseModel
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordRequestForm
import os

app = FastAPI()
manager = LoginManager(str(os.environ.get('SECRET_KEY')), token_url='/auth/token')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class User(BaseModel):
    username: str

class UserDB(User):
    password: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@manager.user_loader()
async def load_user(username: str):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)

@app.post('/auth/token')
async def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = await load_user(username)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(
        data=dict(sub=username)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.post('/register', response_model=User, status_code = status.HTTP_201_CREATED)
async def register(user: UserDB):
    query = users.insert().values(username=user.username, password=user.password)
    last_user_id = await database.execute(query)
    return {**user.dict(), "id": last_user_id}


@app.get("/")
async def read_root(user = Depends(manager)):
    return {"Hello": "World"}