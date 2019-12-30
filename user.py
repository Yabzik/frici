import db

class User():
	def __init__(self, message):
		self.id = message.chat.id
		self.message = message
		self.balance = db.get_user(self.id)['balance']
		self.invited_by = db.get_user(self.id)['invited_by']
		self.ref_code = db.get_user(self.id)['ref_code']
		self.state = db.get_user(self.id)['state']
	
	def addBalance(self, amount):
		db.add_balance(self.id, amount)
		self.balance = self.balance + amount

	def setState(self, state):
		db.change_state(self.id, state)
		self.state = state

	pass





