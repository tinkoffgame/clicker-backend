import flask
import requests

app = flask.Flask(__name__)
GAME_ID = 0
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
API = 'https://api.tinkoffgame.ml/'  # https://api.tinkoffgame.ml/
VALIDATE_API = ''
SCORE_API = 'v1/users/'


#@app.route('/')
#def index():
#    if 'data' in flask.session:
#        return flask.render_template(
#            'index.html',
#            chat_id=flask.session['data']['chat_id'],
#            user_id=flask.session['data']['id'] + 'b'
#        )
#    else:
#        data = {}
#        for data_name in DATA_LIST:
#            data[data_name] = flask.request.args.get(data_name)
#        if data['id']:
#            # TODO: make validation
#            # if api_method(VALIDATE_API, {'data': data})
#
#            flask.session['data'] = data
#            return flask.render_template(
#                'index.html',
#                chat_id=flask.session['data']['chat_id'],
#                user_id=flask.session['data']['id']
#            )
#        else:
#            return 'Auth error'
@app.route('/score/', methods=['GET','POST','PUT'])
def score():
	if flask.request.method == 'PUT':
		score = flask.request.form.get('score')
		user_id = flask.request.form.get('user_id')
		chat_id = flask.request.form.get('chat_id')
		resp = requests.put(API+SCORE_API+user_id, {'score': score, 'game_id': GAME_ID})
		return resp.content
	if flask.request.method == 'POST':
		user_id = flask.request.form.get('user_id')
		chat_id = flask.request.form.get('chat_id')
		resp = requests.post(API+SCORE_API, {'game_id': GAME_ID, 'user_id': user_id, 'chat_id': chat_id})
		return resp.content
	if flask.request.method == 'GET':
		user_id = flask.request.form.get('user_id')
		chat_id = flask.request.form.get('chat_id')
		resp = requests.get(API+SCORE_API, {'game_id': GAME_ID, 'user_id': user_id, 'chat_id': chat_id})
		return resp.content


if __name__ == '__main__':
    print('Hello!')
    # TODO: make secret key secret
    app.secret_key = 'asdfghjklqwertyuiopzxcvbnm'
    app.run()
