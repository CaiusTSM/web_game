from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
	return render_template('index.html')

@socketio.on('connect')
def connection():
	emit('chat message', 'New connection...', broadcast=True)
	
@socketio.on('disconnect')
def connection():
	emit('chat message', 'Connection closed...', broadcast=True)

@socketio.on('chat message')
def test_message(message):
	emit('chat message', message, broadcast=True)

if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0', port=8080)