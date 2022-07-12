import requests
import uvicorn
from fastapi import FastAPI, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

API = "http://7885-188-170-214-41.ngrok.io"
GAME_ID = 1
SCORE_API = "/api/v1/users"
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AuthBase(BaseModel):
    telegram_id: str
    first_name: str
    last_name: str
    chat_id: str


@app.post("/api/v1/auth")
async def authorization(model_in: AuthBase):
    name = model_in.first_name + ' ' + model_in.last_name
    resp = requests.post(API + SCORE_API, json={'game_id': GAME_ID,
                                                'telegram_id': model_in.telegram_id,
                                                'chat_id': model_in.chat_id,
                                                'name': name}).json()
    print(resp)
    return resp


class UpdateUser(BaseModel):
    score: str
    telegram_id: str


@app.put("/api/v1/users")
def update_user(model_in: UpdateUser):
    resp_json = requests.put(API + SCORE_API, json={'game_id': GAME_ID,
                                                    'telegram_id': model_in.telegram_id,
                                                    'score': int(model_in.score)}).json()
    print(resp_json)
    return resp_json


@app.post("/api/v1/users")
def create_user(model_in: AuthBase):
    name = f"{model_in.first_name} {model_in.last_name}"
    resp_json = requests.post(API + SCORE_API, json={'game_id': GAME_ID,
                                                     'telegram_id': model_in.telegram_id,
                                                     'chat_id': model_in.chat_id,
                                                     'name': name}).json()
    print(resp_json)
    return resp_json


class GetUser(BaseModel):
    telegram_id: str
    chat_id: str


@app.get('/api/v1/users')
def get_user(model_in: GetUser):
    resp_json = requests.get(API + SCORE_API, params={'game_id': GAME_ID,
                                                      'telegram_id': model_in.telegram_id,
                                                      'chat_id': model_in.chat_id}).json()
    return resp_json


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, reload=False)
