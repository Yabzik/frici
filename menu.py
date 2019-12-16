import telebot
import db
import msg

from telebot import types
bot = telebot.AsyncTeleBot("605894746:AAHprnzygPIMD0yBCeecyC0kYehYKBWoOQ0")

#создание страницы меню
class MainPage():
	def __init__(self):
		#инициализация кнопок ебучих
		self.profileButton = msg.personal
		self.infoButton = msg.info
		self.buyButton = msg.buy
		self.sellButton = msg.sell
		self.supportButton = msg.support

		#лист текста кнопок(для проверки в хендлере)
		self.msgList = [self.profileButton, self.infoButton, 
				  self.buyButton, self.sellButton, self.supportButton]

		#создание хуйни этой для отображения кнопок
		self.markup = types.ReplyKeyboardMarkup(row_width=2)

		#закидываем кнопки в хуйню для отображения(согласен, выглядит неочень)
		self.markup.row(types.KeyboardButton(self.profileButton))
		self.markup.row(types.KeyboardButton(self.buyButton),
				 types.KeyboardButton(self.sellButton))
		self.markup.row(types.KeyboardButton(self.infoButton))
		self.markup.row(types.KeyboardButton(self.supportButton))
	
	#что же будет делать кнопка при нажатии?????????
	def onPressButton(self, button, message):
		if button == self.profileButton:
			bot.reply_to(message, 'personal')
		elif button == self.buyButton:
			#тут переход на другую страницу
			db.change_state(message.chat.id, 'shop')

			#обновление страницы
			bot.reply_to(message, "Вы ушли в шоп", reply_markup = 
			  Page(db.get_user(message.chat.id)['state']).getMarkup())
			pass
		elif button == self.sellButton:
			pass
		elif button == self.infoButton:
			bot.send_message(message.chat.id, 
					'{} \n {}'.format(msg.info_text,
					  db.get_user(message.chat.id)['balance']))
		elif button == self.supportButton:
			db.change_state(message.chat.id, 'support')
			bot.reply_to(message, "Все Ваши сообщения, отправленные после этого будут переданы администрации\nДля завершения нажмите на кнопку 'Завершить'", reply_markup = 
			  Page(db.get_user(message.chat.id)['state']).getMarkup())

class ShopPage():
	def __init__(self):
		#инициализация кнопок ебучих
		self.beerButton = 'Пиво'
		self.vodkaButton = 'Водка'
		self.backButton = 'В мейн'

		#лист текста кнопок(для проверки в хендлере)
		self.msgList = [self.beerButton, self.vodkaButton, self.backButton]

		#создание хуйни этой для отображения кнопок
		self.markup = types.ReplyKeyboardMarkup(row_width=2)

		#закидываем кнопки в хуйню для отображения(согласен, выглядит неочень)
		self.markup.row(types.KeyboardButton(self.beerButton),
				 types.KeyboardButton(self.vodkaButton))
		self.markup.row(types.KeyboardButton(self.backButton))
	
	#что же будет делать кнопка при нажатии?????????
	def onPressButton(self, button, message):
		if button == self.beerButton:
			bot.reply_to(message, 'Вы купили пиво')
		elif button == self.vodkaButton:
			bot.reply_to(message, 'Вы купили водку')
			pass
		elif button == self.backButton:
			#тут переход на другую страницу
			db.change_state(message.chat.id, 'main')
			
			#обновление страницы
			bot.reply_to(message, "Вы ушли в шоп", reply_markup = 
			  Page(db.get_user(message.chat.id)['state']).getMarkup())
			pass	

class SupportPage():
	def __init__(self):
		#инициализация кнопки ебнутой
		self.completeButton = 'Завершить'

		#лист текста кнопок(для проверки в хендлере)
		self.msgList = [self.completeButton]

		#создание хуйни этой для отображения кнопок
		self.markup = types.ReplyKeyboardMarkup(row_width=1)

		#закидываем кнопки в хуйню для отображения(согласен, выглядит неочень)
		self.markup.row(types.KeyboardButton(self.completeButton))
	
	#что же будет делать кнопка при нажатии?????????
	def onPressButton(self, button, message):
		if button == self.completeButton:
			db.change_state(message.chat.id, 'main') #переход на другую станицу
			bot.reply_to(message, "Спасибо! После рассмотрения обращения мы ответим Вам", reply_markup = 
			  Page(db.get_user(message.chat.id)['state']).getMarkup())

class Page():

	#инициализация страницы в зависимости от входящего стринга из ДБ
	def __init__(self, pageName):
		self.page_name = pageName
		if pageName == 'main':
			self.page = MainPage()
		elif pageName == 'shop':
			self.page = ShopPage()
		elif pageName == 'support':
			self.page = SupportPage()

	def getMarkup(self):
		return self.page.markup

	def pressButton(self, message):
		return self.page.onPressButton(message.text, message)

	#проверка на наличие кнопки
	def isValidMessage(self, message):
		if any(item in message.text for item in self.page.msgList):
			return True
		else:
			return False
	pass
