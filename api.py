import requests
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

API = "https://api.tinkoffgame.ml"
GAME_ID = 1
SCORE_API = "/api/v1/users"
TABLE_API = "/api/v1/table"
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["*"],
)
score = dict()


class GetUser(BaseModel):
    telegram_id: str
    chat_id: str


class UpdateTable(BaseModel):
    telegram_id: str
    score: int


class AuthBase(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str
    chat_id: int


@app.post("/api/v1/auth")
async def authorization(model_in: AuthBase):
    name = f"{model_in.first_name} {model_in.last_name}"
    requests.post(API + SCORE_API, json={'game_id': GAME_ID,
                                         'telegram_id': model_in.telegram_id,
                                         'chat_id': model_in.chat_id,
                                         'name': name})
    score[int(model_in.telegram_id)] = 0
    print(score)
    print(model_in.telegram_id)
    resp_json = requests.get(API + TABLE_API, params={
        "game_id": GAME_ID,
        "chat_id": model_in.chat_id
    }).json()
    return resp_json


@app.put("/api/v1/score")
def update_user(model_in: UpdateTable):
    print(score)
    print(model_in.telegram_id)
    if model_in.score <= 60:
        score[int(model_in.telegram_id)] += model_in.score
    return {"score_now": score[int(model_in.telegram_id)]}


@app.put("/api/v1/users")
def update_user(model_in: UpdateTable):
    print(score)
    print(model_in.telegram_id)
    if model_in.score < 60:
        score[int(model_in.score)] += model_in.score
        resp_json = requests.put(API + SCORE_API,
                                 json={'game_id': GAME_ID,
                                       'telegram_id': model_in.telegram_id,
                                       'score': int(
                                           score[
                                               int(model_in.telegram_id)])}).json()
        score.pop(int(model_in.telegram_id), None)
        return resp_json


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, reload=False)
