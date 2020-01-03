import telebot
import db
import msg

from telebot import types
from user import User
from saleApplication import SaleApp

bot = telebot.AsyncTeleBot("605894746:AAHprnzygPIMD0yBCeecyC0kYehYKBWoOQ0")

#создание страницы меню
class MainPage():
	def __init__(self, user):
		#колхозная проверка на наличии альтернативной обработки
		#сообщения у страницы(временно)
		self.isExtended = False	
	
		#инициализируем пользователя
		self.user = user

		#инициализация кнопок 
		self.profileButton = msg.personal
		self.infoButton = msg.info
		self.buyButton = msg.buy
		self.sellButton = msg.sell
		self.supportButton = msg.support

		#лист текста кнопок(для проверки в хендлере)
		self.msgList = [self.profileButton, self.infoButton, 
				  self.buyButton, self.sellButton, self.supportButton]

		#создание объекта для отображения кнопок
		self.markup = types.ReplyKeyboardMarkup(row_width=2)

		#закидываем кнопки в объект для отображения
		self.markup.row(types.KeyboardButton(self.profileButton))
		self.markup.row(types.KeyboardButton(self.buyButton),
				 types.KeyboardButton(self.sellButton))
		self.markup.row(types.KeyboardButton(self.infoButton))
		self.markup.row(types.KeyboardButton(self.supportButton))
	
	#что же будет делать кнопка при нажатии?????????
	def onPressButton(self):
		button = self.user.message.text

		if button == self.profileButton:
			markup = telebot.types.InlineKeyboardMarkup()
			button = telebot.types.InlineKeyboardButton(text='Пригласить друга', callback_data='invite_message')
			markup.add(button)
			bot.send_message(self.user.message.chat.id, '💎 Баланс: {}\n'
														'🛒 Покупок: {}\n'
														'💰 Продаж: {}'.format(self.user.balance, db.get_purchases(self.user.id), db.get_sells(self.user.id)),
														reply_markup=markup)
		elif button == self.buyButton:
			#тут переход на другую страницу
			self.user.setState('shop')

			#обновление страницы
			bot.reply_to(self.user.message, "Вы ушли в шоп", reply_markup = 
			  Page(self.user).getMarkup())
			pass
		elif button == self.sellButton:
			#тут переход на другую страницу
			self.user.setState('sale')

			#обновление страницы
			bot.reply_to(self.user.message, "Вы зашли в создание товара на продажу, если Вы передумали что-либо продавать или ввели неккоректные данные, нажмите кнопку Отмена. После создания заявки на продажу, модераторы проверят её и Ваш товар станет доступен для покупки другим пользователям. Статус обработки заявки можно посмотреть где-то.", reply_markup = 
			  Page(self.user).getMarkup()).wait()

			bot.send_message(self.user.id, "Напишите название вашего товара")
			pass
		elif button == self.infoButton:
			bot.send_message(self.user.id, 
					'{} \n {}'.format(msg.info_text, self.user.balance))
		elif button == self.supportButton:
			self.user.setState('support')
			
			bot.reply_to(self.user.message, "Все Ваши сообщения, отправленные после этого будут переданы администрации\nДля завершения нажмите на кнопку 'Завершить'", reply_markup = 
			  Page(self.user).getMarkup())

class ShopPage():
	def __init__(self, user):
		#колхозная проверка на наличии альтернативной обработки
		#сообщения у страницы(временно)
		self.isExtended = False

		#инициализируем пользователя
		self.user = user

		#инициализация кнопок 
		self.beerButton = 'Пиво'
		self.vodkaButton = 'Водка'
		self.backButton = 'В мейн'

		#лист текста кнопок(для проверки в хендлере)
		self.msgList = [self.beerButton, self.vodkaButton, self.backButton]

		#создание объекта для отображения кнопок
		self.markup = types.ReplyKeyboardMarkup(row_width=2)

		#закидываем кнопки в объект для отображения
		self.markup.row(types.KeyboardButton(self.beerButton),
				 types.KeyboardButton(self.vodkaButton))
		self.markup.row(types.KeyboardButton(self.backButton))
		self.markup.row(types.KeyboardButton('suchka'))
	
	#что же будет делать кнопка при нажатии?????????
	def onPressButton(self):
		button = self.user.message.text

		if button == self.beerButton:
			bot.reply_to(self.user.message, 'Вы купили пиво')
		elif button == self.vodkaButton:
			bot.reply_to(self.user.message, 'Вы купили водку')
			pass
		elif button == self.backButton:
			#тут переход на другую страницу
			self.user.setState('main')
			
			#обновление страницы
			bot.reply_to(self.user.message, "Вы ушли в мейн", reply_markup = 
			  Page(self.user).getMarkup())
			pass	

class SupportPage():
	def __init__(self, user):
		#колхозная проверка на наличии альтернативной обработки
		#сообщения у страницы(временно)
		self.isExtended = True

		#инициализируем пользователя
		self.user = user

		#инициализация кнопок 
		self.completeButton = 'Завершить'

		#лист текста кнопок(для проверки в хендлере)
		self.msgList = [self.completeButton]

		#создание объекта для отображения кнопок
		self.markup = types.ReplyKeyboardMarkup(row_width=1)

		#закидываем кнопки в объект для отображения
		self.markup.row(types.KeyboardButton(self.completeButton))
	

	#что же будет делать кнопка при нажатии?????????
	def onPressButton(self):
		button = self.user.message.text

		if button == self.completeButton:
			self.user.setState('main') #переход на другую станицу

			bot.reply_to(self.user.message, "Спасибо! После рассмотрения обращения мы ответим Вам", reply_markup = 
			  Page(self.user).getMarkup())

	def Think(self):
		db.open_support(self.user.id)
		db.send_to_support(self.user.id, self.user.message.text)

class SalePage():
	def __init__(self, user):
		#колхозная проверка на наличии альтернативной обработки
		#сообщения у страницы(временно)
		self.isExtended = True

		#инициализируем пользователя
		self.user = user

		#инициализация заявки из бд
		self.saleApp = SaleApp(self.user)

		#инициализация кнопок 
		self.cancel = 'Отмена'

		#лист текста кнопок(для проверки в хендлере)
		self.msgList = [self.cancel]

		#создание объекта для отображения кнопок
		self.markup = types.ReplyKeyboardMarkup(row_width=2)

		#закидываем кнопки в объект для отображения
		self.markup.row(types.KeyboardButton(self.cancel))
		
	#что же будет делать кнопка при нажатии?????????
	def onPressButton(self):
		button = self.user.message.text
	
		if button == self.cancel:
			#удаляем заявку
			self.saleApp.delete()

			#тут переход на другую страницу
			self.user.setState('main')

			#обновление страницы
			bot.reply_to(self.user.message, "Вы ушли в главное меню", reply_markup = 
			  Page(self.user).getMarkup())
			pass

	def Think(self):
		
		if self.saleApp.title == 'None':
			self.saleApp.setTitle(self.user.message.text)

			#это сообщение оповещает юзера про то что следующая обработка - это елиф ниже данного коммента
			bot.send_message(self.user.id, "Напишите описание к вашему товару")
		elif self.saleApp.description == 'None':
			self.saleApp.setDesc(self.user.message.text)
			bot.send_message(self.user.id, "Отправьте фотографии товара (все одним сообщением)")
		elif not self.saleApp.photos or self.user.message.content_type == 'photo':
			fileID = self.user.message.photo[-1].file_id
			file = bot.get_file(fileID).wait()
			pic = bot.download_file(file.file_path).wait()
			self.saleApp.addPhoto(pic)
			bot.send_message(self.user.id, "Напишите цену вашего товара")
		elif not self.saleApp.price:
			self.saleApp.setPrice(self.user.message.text)
			
			#смена статуса на "проверяется"
			self.saleApp.setStatus('checking')

			self.user.setState('main') #переход на другую станицу

			#обновление страницы
			bot.reply_to(self.user.message, "Ваша заявка отправлена в обработку", reply_markup = 
			  Page(self.user).getMarkup())

		pass

	def _isEmpty():
		pass


class Page():
	#инициализация страницы в зависимости от входящего стринга из ДБ
	def __init__(self, user):
		self.user = user
		self.page_name = user.state

		if self.page_name == 'main':
			self.page = MainPage(user)
		elif self.page_name == 'shop':
			self.page = ShopPage(user)
		elif self.page_name == 'support':
			self.page = SupportPage(user)
		elif self.page_name == 'sale':
			self.page = SalePage(user)

	

	def getMarkup(self):
		return self.page.markup

	def handleMessage(self):
		if self.user.message.content_type == 'photo':
			if self.page_name == 'sale':
				self.page.Think()
		elif self.__isButton(self.user.message):
		    self.page.onPressButton()
			#новая проверка,  может ли страница обрабатывать что-то кроме кнопки
		elif self.page.isExtended:
			self.page.Think()

			#проверка на наличие кнопки
	def __isButton(self, message):
		if any(item in message.text for item in self.page.msgList):
			return True
		else:
			return False
	pass
	
