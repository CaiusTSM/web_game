from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os
from game_server import *
from game import GameJSONEncoder

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.json_encoder = GameJSONEncoder

socketio = SocketIO(app)

game_server = GameServer(socketio, threaded=True)

clients = {}

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/game.js')
def game_js():
	return render_template('game.js')

@socketio.on('connect')
def connect():
	player_uid = game_server.add_player('guest')
	clients[request.sid] = player_uid
	
	emit('chat message', '' + 'guest' + ' connected...', broadcast=True)
	
@socketio.on('disconnect')
def disconnect():
	uid = clients[request.sid]
	player_name = game_server.get_player_name(uid)
	
	game_server.remove_player(uid)
	del clients[request.sid]

	emit('chat message', '' + player_name + ' disconnected...', broadcast=True)

@socketio.on('chat message')
def chat_message(message):
	uid = clients[request.sid]
	player_name = game_server.get_player_name(uid)

	if len(message) > 6 and message.startswith('/name '):
		new_name = message[6:]
		game_server.set_player_name(uid, new_name)
		emit('chat message', '' + player_name + ' set name to ' + new_name, broadcast=True)
	else:
		emit('chat message', '' + player_name + ': ' + message, broadcast=True)

if __name__ == '__main__':
	try:
		game_server.start()
		socketio.run(app, host='0.0.0.0', port=8080)
	finally:
		game_server.stop()