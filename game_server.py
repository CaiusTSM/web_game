import threading
import time

from game import *

# gets the miliseconds passed since 19XX (don't remember / does not matter)
def current_time():
	return int(round(time.time() * 1000))

class GameServer:
	def __init__(self, socketio, threaded=False):
		self.socketio = socketio
		self.threaded = threaded
		self.thread = None
		self.lock_game = None
		if threaded == True:
			self.lock_game = threading.Lock()
		self.game = Game()
		self.running = False
		self.last_time = 0
		self.time_passed = 0
		# timestep is 1/60th (60 FPS) of a second in miliseconds
		self.time_step = (1.0 / 60.0) * 1000.0
		self.max_tick_count = 10
		# send state of server to clients 20 times per second
		self.sample_time = (1.0 / 20.0) * 1000.0
		self.sample_timer = 0
	
	def get_game_lock(self):
		return self.lock_game
		
	def start(self):
		if self.threaded == True:
			self.thread = threading.Thread(target=self.run)
			self.thread.start()
		else:
			self.run()
			
	def stop(self):
		self.running = False
		if self.threaded == True:
			self.thread.join()
		
	def run(self):
		# init
		self.running = True
		self.last_time = current_time()
		self.time_passed = 0
		# main game loop
		while self.running == True:
			delta_time = current_time() - self.last_time
			self.last_time = current_time()
			self.time_passed += delta_time
			self.sample_timer += delta_time
			tick_count = 0
			while self.time_passed >= self.time_step and tick_count < self.max_tick_count:
				self.tick()
				self.time_passed -= self.time_step
				tick_count += 1
				if tick_count == self.max_tick_count:
					self.time_passed = 0
			if self.sample_timer >= self.sample_time:
				self.socketio.emit('game state', '__game state__ --- ' + str(current_time()))
				self.sample_timer = 0
			if tick_count > 1:
				print("WARNING: Game is running slow.")
	
	def tick(self):
		if self.threaded == True:
			self.lock_game.acquire()
			try:
				self.game.tick(self.time_step)
			finally:
				self.lock_game.release()
		else:
			self.game.tick(self.time_step)
	
	def spawn_player(self, username):
		player_uid = ""
		if self.threaded == True:
			self.lock_game.acquire()
			try:
				player_uid = self.game.spawn_player(username)
			finally:
				self.lock_game.release()
		else:
			player_uid = self.game.spawn(username)
		return player_uid
			
	def set_player_name(self, uid, username):
		if self.threaded == True:
			self.lock_game.acquire()
			try:
				self.game.set_player_name(uid, username)
			finally:
				self.lock_game.release()
		else:
			self.game.set_player_name(uid, username)
			
	def get_player_name(self, uid):
		return self.game.get_player_name(uid)
		
	def get_game_state(self):
		return self.game.get_game_state()