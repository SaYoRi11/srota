import os

from fastapi import FastAPI, status, Depends, Query
from fastapi_login import LoginManager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Union

from db import database, users
from utils import get_es

tags_metadata = [
    {
        "name": "test",
        "description": "Test if the API is working correctly"
    },
    {
        "name": "auth",
        "description": "Register and authentication endpoints"
    },
    {
        "name": "series",
        "description": "Get the series by series id and filter using different queries."
    }
]

app = FastAPI(
    title="Srota",
    description="Srota API",
    version="1.0.0",
    openapi_tags=tags_metadata
)
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

@app.post('/auth/token', tags=["auth"])
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

@app.post('/register', response_model=User, status_code = status.HTTP_201_CREATED, tags=["auth"])
async def register(user: UserDB):
    query = users.insert().values(username=user.username, password=user.password)
    last_user_id = await database.execute(query)
    return {**user.dict(), "id": last_user_id}


@app.get("/", tags=["test"])
async def read_root(user=Depends(manager)):
    es = get_es()
    if es.ping():
        return {"Hello": "World"}

@app.get("/series/{series_id}", tags=["series"])
async def get_series(
    series_id:str, 
    start:int = 0, 
    limit:int = 100, 
    location: Union[str, None] = Query(default=None, example='Kathmandu', max_length=50), 
    date_start: Union[str, None] = Query(default=None, example='2017-01-01 00:00:00'), 
    date_end: Union[str, None] = Query(default=None, example='2020-01-01 00:00:00'), 
    driver_fled:bool = False, 
    caused_death:bool = False,
    desc:bool = True,
    user=Depends(manager)
):
    es = get_es()
    search_body = []

    if location:
        search_body.append({
                    "multi_match": {
                        "query": location,
                        "fields": ["locations.primary.name", "locations.primary.province.name", "locations.primary.district.name"]
                    }
        })

    if date_start or date_end:
        date = {
                "range": {
                    "published_at": {}
                }
            }
        if date_start:
            date["range"]["published_at"]["gte"] = date_start
        if date_end:
            date["range"]["published_at"]["lte"] = date_end
        search_body.append(date)

    if driver_fled or caused_death:
        nested = {
                "nested": {
                    "path": "graph",
                    "query": {
                        "bool": {
                            "must": []
                        }
                    }
                }
            
        }
        if driver_fled:
            nested['nested']['query']['bool']['must'].append({
                                "match": {
                                    "graph.onto:driverFled": True
                                }
                            })
        if caused_death:
            nested['nested']['query']['bool']['must'].append({
                                "match": {
                                    "graph.onto:caused": "srota:Death"
                                }
                            })
        search_body.append(nested)
        
    res = es.search({
        "query": {
            "bool": {
                "must": search_body,
                "filter": {
                    "term": {
                        "lineage.series": f"http://series/{series_id}"
                    }
                }
            }
        },
        'sort': [
				{'published_at': {'order': 'desc' if desc else 'asc'}}
			],
		'from': start,
		'size': min(1000, limit)
    })
    return res["hits"]
