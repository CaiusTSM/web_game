from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os
from game_server import *
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

game_server = GameServer(socketio, threaded=True)

clients = {}

@app.route('/')
def index():
	return render_template('index.html')

@socketio.on('connect')
def connect():
	player_uid = game_server.spawn_player('guest')
	clients[request.sid] = player_uid
	
	emit('chat message', '' + 'guest' + ' connected...', broadcast=True)
	
@socketio.on('disconnect')
def disconnect():
	player_name = game_server.get_player_name(clients[request.sid])
	
	del clients[request.sid]

	emit('chat message', '' + player_name + ' disconnected...', broadcast=True)

@socketio.on('chat message')
def chat_message(message):
	player_name = game_server.get_player_name(clients[request.sid])

	if len(message) > 6 and message.startswith('/name '):
		new_name = message[6:]
		game_server.set_player_name(clients[request.sid], new_name)
		emit('chat message', '' + player_name + ' set name to ' + new_name, broadcast=True)
	else:
		emit('chat message', '' + player_name + ': ' + message, broadcast=True)

if __name__ == '__main__':
	try:
		game_server.start()
		socketio.run(app, host='0.0.0.0', port=8080)
	finally:
		game_server.stop()