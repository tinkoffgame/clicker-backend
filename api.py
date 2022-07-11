import requests
import uvicorn
from fastapi import FastAPI, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

API = "http://localhost:5000"
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
    username: str
    photo_url: str
    auth_date: str
    hash: str
    chat_id: str


@app.post("api/v1/auth/")
async def authorization(model_in: AuthBase, response: Response):
    for key, val in model_in.dict().items():
        response.set_cookie(key=str(key.encode('utf_8')),
                            value=str(val.encode('utf_8')),
                            httponly=True)
    name = model_in.first_name + ' ' + model_in.last_name
    resp = requests.post(API + SCORE_API, json={'game_id': GAME_ID,
                                                'telegram_id': model_in.telegram_id,
                                                'chat_id': model_in.chat_id,
                                                'name': name}).json()
    print(resp)
    return resp


@app.put("/api/v1/users/")
def update_user(score: int,
                telegram_id: Cookie(None)):
    resp_json = requests.put(API + SCORE_API, json={'game_id': GAME_ID,
                                                    'telegram_id': telegram_id,
                                                    'score': score}).json()
    print(resp_json)
    return resp_json


@app.post("/api/v1/users/")
def create_user(chat_id: Cookie(None),
                telegram_id: Cookie(None),
                first_name: Cookie(None),
                last_name: Cookie(None)):
    name = f"{first_name} {last_name}"
    resp_json = requests.post(API + SCORE_API, json={'game_id': GAME_ID,
                                                     'telegram_id': telegram_id,
                                                     'chat_id': chat_id,
                                                     'name': name}).json()
    print(resp_json)
    return resp_json


@app.get('/api/v1/users/')
def get_user(telegram_id: Cookie(None),
             chat_id: Cookie(None)):
    resp_json = requests.get(API + SCORE_API, params={'game_id': GAME_ID,
                                                      'telegram_id': telegram_id,
                                                      'chat_id': chat_id}).json()
    return resp_json


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, reload=False)
