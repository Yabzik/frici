import db

#rom user import User

class SaleApp():

	def __init__(self, user):

		if not db.get_sale_app(user.id):
			db.add_sale_app(user.id)
			
		saleApp = db.get_sale_app(user.id)
		self.id = saleApp['id']
		self.title = saleApp['title']
		self.description = saleApp['description']
		self.price = saleApp['price']
		self.seller = saleApp['seller']
		self.status = saleApp['status']

		self.photos = db.get_sale_app_photos(self.id)
	
	def setTitle(self, title):
		db.add_sale_app_title(self.id, title)
		self.title = title

	def setDesc(self, desc):
		db.add_sale_app_desc(self.id, desc)
		self.description = desc

	def setPrice(self, price):
		db.add_sale_app_price(self.id, price)
		self.price = price

	def setStatus(self, status):
		db.set_sale_app_status(self.id, status)
		self.status = status

	def addPhoto(self, photo):
		db.add_sale_app_photo(self.id, photo)
		#self.photos.append(photo)

	def delete(self):
		db.del_sale_app(self.id)

		
