import db

class User():
	def __init__(self, id):
		self.id = id
		self.balance = db.get_user(id)['balance']
		self.invited_by = db.get_user(id)['invited_by']
		self.ref_code = db.get_user(id)['ref_code']
	
	def increment_balance(self, var):
		self.balance += var
	pass




