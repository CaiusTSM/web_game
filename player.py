class Player:
	def __init__(self, uid, username):
		self.uid = uid
		self.username = username
		
	def get_uid(self):
		return self.uid
		
	def set_name(self, username):
		self.username = username
		
	def get_name(self):
		return self.username