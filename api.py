import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime

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

requests_list = dict()

class GetUser(BaseModel):
    telegram_id: int
    chat_id: int


class UpdateUser(BaseModel):
    telegram_id: int
    score: int


class AuthBase(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str
    chat_id: int


@app.post("/api/v1/auth")
async def authorization(model_in: AuthBase, telegram_id: int):
    if model_in.telegram_id != telegram_id:
        raise HTTPException(status_code=401)
    
    if (not telegram_id in requests_list):
        requests_list[telegram_id] = {
            'last_request': datetime.datetime.now(),
            'ban': False
        }
    else:
        requests_list[telegram_id]['last_request'] = datetime.datetime.now()
        ban = requests_list[telegram_id]['ban'] 
        if (ban != False):
            t = ban + datetime.timedelta(minutes=10)
            if (datetime.datetime.now() > t):
                requests_list[telegram_id]['ban'] = False
            else:
                score[telegram_id] = 0
                t += datetime.timedelta(hours=3)
                raise HTTPException(429, detail={
                    'unban': t.strftime('%d.%m.%Y %H:%M:%S')
                })
    
    name = f"{model_in.first_name} {model_in.last_name}"
    requests.post(API + SCORE_API, json={'game_id': GAME_ID,
                                         'telegram_id': model_in.telegram_id,
                                         'chat_id': model_in.chat_id,
                                         'name': name})
    score[model_in.telegram_id] = 0
    resp_json = requests.get(API + TABLE_API, params={
        "game_id": GAME_ID,
        "chat_id": model_in.chat_id
    }).json()
    return resp_json


@app.put("/api/v1/score")
def update_user(model_in: UpdateUser, telegram_id: int):
    if model_in.telegram_id != telegram_id:
        raise HTTPException(status_code=401)
    
    print(requests_list)
    
    if (not telegram_id in requests_list):
        requests_list[telegram_id] = {
            'last_request': datetime.datetime.now(),
            'ban': False
        }
    else:
        lr = requests_list[telegram_id]['last_request']    
        if (lr + datetime.timedelta(seconds=2) > datetime.datetime.now()):
            ban = datetime.datetime.now()
            requests_list[telegram_id]['ban'] = ban
            t = ban + datetime.timedelta(minutes=10)
            score[telegram_id] = 0
            t += datetime.timedelta(hours=3)
            raise HTTPException(429, detail={
                    'unban': t.strftime('%d.%m.%Y %H:%M:%S')
                })
            
        requests_list[telegram_id]['last_request'] = datetime.datetime.now()
        ban = requests_list[telegram_id]['ban'] 
        if (ban != False):
            t = ban + datetime.timedelta(minutes=10)
            if (datetime.datetime.now() > t):
                requests_list[telegram_id]['ban'] = False
            else:
                score[telegram_id] = 0
                t += datetime.timedelta(hours=3)
                raise HTTPException(429, detail={
                    'unban': t.strftime('%d.%m.%Y %H:%M:%S')
                })
    
                
    if model_in.score <= 60:
        score[model_in.telegram_id] += model_in.score
    return {"score_now": score[model_in.telegram_id]}


@app.put("/api/v1/users")
def update_user(model_in: UpdateUser, telegram_id: int):
    if model_in.telegram_id != telegram_id:
        raise HTTPException(status_code=401)
    
    if (not telegram_id in requests_list):
        requests_list[telegram_id] = {
            'last_request': datetime.datetime.now(),
            'ban': False
        }
    else:
        requests_list[telegram_id]['last_request'] = datetime.datetime.now()
        ban = requests_list[telegram_id]['ban'] 
        if (ban != False):
            t = ban + datetime.timedelta(minutes=10)
            if (datetime.datetime.now() > t):
                requests_list[telegram_id]['ban'] = False
            else:
                score[telegram_id] = 0
                t += datetime.timedelta(hours=3)
                raise HTTPException(429, detail={
                    'unban': t.strftime('%d.%m.%Y %H:%M:%S')
                })
                
    if model_in.score <= 60:
        temp_score = score[model_in.telegram_id] + model_in.score
        score.pop(model_in.telegram_id, None)
        resp_json = requests.put(API + SCORE_API,
                                 json={'game_id': GAME_ID,
                                       'telegram_id': model_in.telegram_id,
                                       'score': int(temp_score)}).json()
        return resp_json


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, reload=True)
