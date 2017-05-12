import uuid
import json

from player import *

class GameJSONEncoder(json.JSONEncoder):
	def default(self, obj):
		return obj.__dict__
	
		#return json.JSONEncoder.default(self, obj)

class Game:
	def __init__(self):
		self.players = []
		
	def tick(self, time_step):
		pass
		
	def add_player(self, username):
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