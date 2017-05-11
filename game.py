import uuid

from player import *

class Game:
	def __init__(self):
		self.players = []
		self.blah = 0
		
	def tick(self, time_step):
		self.blah += 1
		
	def spawn_player(self, username):
		new_player = Player(str(uuid.uuid4()), username)
		self.players.append(new_player)
		return new_player.get_uid()
		
	def remove_player(self, uid):
		for player in self.players:
			if player.get_uid() == uid:
				self.players.remove(player)
				break
		
	def set_player_name(self, uid, username):
		for player in self.players:
			if player.get_uid() == uid:
				player.set_name(username)
				break
	
	def get_player_name(self, uid):
		name = ""
		for player in self.players:
			if player.get_uid() == uid:
				name = player.get_name()
				break
		return name
		
	def get_game_state(self):
		state = {}
		state['players'] = self.players
		return state