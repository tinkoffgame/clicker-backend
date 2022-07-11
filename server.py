import flask
import requests
import secrets2
import json
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
GAME_ID = 1
DATA_LIST = [
    'id',
    'first_name',
    'last_name',
    'username',
    'photo_url',
    'auth_date',
    'hash',
    'chat_id'
]
# API = 'https://api.tinkoffgame.ml/'
API = 'http://064e-188-170-214-41.ngrok.io/'
SCORE_API = 'api/v1/users/'


@app.route("/index", methods=['POST', 'GET'])
@cross_origin()
def index():
    return "hello"


@app.route('/api/v1/auth/', methods=['POST', 'OPTIONS'])
@cross_origin()
def auth():
    if flask.request.method == 'OPTIONS':
        return 'OK'
    if flask.request.method == "POST":
        data = {}
        print(flask.request.headers)
        json1 = flask.request.data
        json1 = json.loads(json1)
        for data_name in DATA_LIST:
            data[data_name] = json1.get(data_name)
        if data['id']:
            # TODO: make validation

            flask.session['data'] = data

            telegram_id = flask.session['data']['id']
            chat_id = flask.session['data']['chat_id']
            name = flask.session['data']['first_name'] + ' ' + \
                   flask.session['data']['last_name']

            resp = requests.post(API + SCORE_API, json={'game_id': GAME_ID,
                                                        'telegram_id': telegram_id,
                                                        'chat_id': chat_id,
                                                        'name': name}).json()
            print(resp)
            return resp
        else:
            return str(400)


@app.route('/api/v1/users/', methods=['GET', 'POST', 'PUT'])
@cross_origin()
def users():
    if flask.request.method == 'PUT':
        score = flask.request.get_json().get('score')
        telegram_id = flask.session['data']['id']

        # telegram_id = flask.request.form.get('telegram_id')
        print(score, telegram_id)
        resp = requests.put(API + SCORE_API, json={'game_id': GAME_ID,
                                                   'telegram_id': telegram_id,
                                                   'score': score})
        return resp.content

    if flask.request.method == 'POST':
        telegram_id = flask.session['data']['id']
        chat_id = flask.session['data']['chat_id']
        name = flask.session['data']['first_name'] + ' ' + \
               flask.session['data']['last_name']

        # telegram_id = flask.request.form.get('telegram_id')
        # chat_id = flask.request.form.get('chat_id')
        # first_name = flask.request.form.get('first_name') + ' ' + flask.request.form.get('last_name')

        resp = requests.post(API + SCORE_API, json={'game_id': GAME_ID,
                                                    'telegram_id': telegram_id,
                                                    'chat_id': chat_id,
                                                    'name': name})
        return resp.content

    if flask.request.method == 'GET':
        telegram_id = flask.session['data']['id']
        chat_id = flask.session['data']['chat_id']
        # telegram_id = flask.request.form.get('telegram_id')
        # chat_id = flask.request.form.get('chat_id')

        resp = requests.get(API + SCORE_API, params={'game_id': GAME_ID,
                                                     'telegram_id': telegram_id,
                                                     'chat_id': chat_id})
        return resp.content


if __name__ == '__main__':
    app.secret_key = secrets2.secret_key
    app.run(host='0.0.0.0', port=5500, debug=True)
