import telebot
import db
import msg
import utils

from telebot import types
from user import User
from saleApplication import SaleApp

import emoji

bot = telebot.AsyncTeleBot("605894746:AAG0WlMjuXoFtKjMOhdhRDkrA-0Ca1uC06I")

# ------ ЛОГИ  ------
import logging
logger = logging.getLogger('Main')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('actions.log')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(file_handler)
# ------ ЛОГИ  ------

#создание страницы меню
class MainPage():
	def __init__(self, user):
		#колхозная проверка на наличии альтернативной обработки
		#сообщения у страницы(временно)
		self.isExtended = True	
	
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
		logger.info('{} - нажата кнопка {}'.format(self.user.message.chat.id, emoji.demojize(button)))
		if button == self.profileButton:
			markup = telebot.types.InlineKeyboardMarkup()
			markup.add(telebot.types.InlineKeyboardButton(text='🛒 Мои покупки', callback_data='my_purchases'))
			markup.add(telebot.types.InlineKeyboardButton(text='💰 Мои продажи', callback_data='my_sales'))
			markup.add(telebot.types.InlineKeyboardButton(text='🤝 Пригласить друга', callback_data='invite_message'))
			markup.add(telebot.types.InlineKeyboardButton(text='🏷 Ввести код купона', callback_data='enter_coupon_code'))
			bot.send_message(self.user.message.chat.id, '💎 Баланс: {}\n'
														'🛒 Покупок: {}\n'
														'💰 Продаж: {}'.format(self.user.balance, db.get_purchases(self.user.id), db.get_sells(self.user.id)),
														reply_markup=markup)
		elif button == self.buyButton:
			#тут переход на другую страницу
			self.user.setState('shop')

			if db.get_selling_products():
				text = 'Товары в продаже:'
				for product in db.get_selling_products():
					text += '\n\n🔹 <b>{}</b>\nЦена: {} 💎\nКупить: /buy_{}'.format(product['title'], product['price'], utils.convertInt(product['id']))
				bot.send_message(self.user.message.chat.id, text, parse_mode='HTML', reply_markup = Page(self.user).getMarkup())
			else:
				bot.send_message(self.user.message.chat.id, 'К сожалению, сейчас ничего нет в продаже. Почему бы не продать что-то?', reply_markup = Page(self.user).getMarkup())
	
		elif button == self.sellButton:
			if db.check_sale_rules(self.user.id) == 1:
				#тут переход на другую страницу
				self.user.setState('sale')

				#обновление страницы
				bot.reply_to(self.user.message, "Вы зашли в создание товара на продажу, если Вы передумали что-либо продавать или ввели неккоректные данные, нажмите кнопку Отмена. После создания заявки на продажу, модераторы проверят её и Ваш товар станет доступен для покупки другим пользователям. Статус обработки заявки можно посмотреть где-то.", reply_markup = 
				  Page(self.user).getMarkup()).wait()

				bot.send_message(self.user.id, "Напишите название вашего товара")
			else:
				markup = telebot.types.InlineKeyboardMarkup()
				markup.add(telebot.types.InlineKeyboardButton(text='Принять соглашение', callback_data='sale_confirm_rules'))
				bot.send_message(self.user.id, 'Перед созданием первого товара Вам нужно ознакомиться с правилами и советами:\n\n'
												'- Товар должен быть размещен на территории школы таким образом, чтобы любой покупатель мог легко его забрать\n'
												'- Сделайте хорошие фотографии с нескольких ракурсов\n'
												'- Составьте подробное описание нахождения товара\n'
												'- После добавления товара не забирайте его и не передавайте никому информацию о его размещении\n\n'
												'- Ваш товар может быть незначительно изменен администрацией в процессе подтверждения', reply_markup=markup)
		elif button == self.infoButton:
			bot.send_message(self.user.id, 
					'{} \n {}'.format(msg.info_text, self.user.balance))
		elif button == self.supportButton:
			self.user.setState('support')
			
			bot.reply_to(self.user.message, "Все Ваши сообщения, отправленные после этого будут переданы администрации\nДля завершения нажмите на кнопку 'Завершить'", reply_markup = 
			  Page(self.user).getMarkup())

	def handleButtonCallback(self, call):
		logger.info('{} - главная страница, колбэк кнопки {}'.format(self.user.message.chat.id, call.data))
		if call.data == 'invite_message':
			bot.answer_callback_query(callback_query_id=call.id)
			markup = telebot.types.InlineKeyboardMarkup()
			markup.add(telebot.types.InlineKeyboardButton(text='Получить ссылку для приглашения', callback_data='invite_get_link'))
			bot.send_message(self.user.message.chat.id, 'Вы можете пригласить друга запустить бота. При этом и Вы и приглашенный друг получите +25 к балансу.',
														reply_markup=markup)
		elif call.data == 'my_purchases':
			bot.answer_callback_query(callback_query_id=call.id)
			if db.get_user_bought_products(self.user.message.chat.id):
				text = 'Мои покупки:'
				for product in db.get_user_bought_products(self.user.message.chat.id):
					text += '\n\n- {}\nЦена: {} 💎'.format(product['title'], product['price'])
				bot.send_message(self.user.message.chat.id, text)
			else:
				bot.send_message(self.user.message.chat.id, 'Вы еще ничего не купили. Почему бы не сделать это прямо сейчас?')
		elif call.data == 'my_sales':
			if db.get_user_sale_products(self.user.message.chat.id):
				text = 'Мои продажи:'
				for product in db.get_user_sale_products(self.user.message.chat.id):
					text += '\n\n- {}\nЦена: {} 💎\nСтатус: {}'.format(product['title'], product['price'], utils.status[product['status']])
				bot.send_message(self.user.message.chat.id, text)
			else:
				bot.send_message(self.user.message.chat.id, 'У вас нет товаров, размещенных для продажи. Может стоит продать что-то?')
		elif call.data == 'invite_get_link':
			bot.answer_callback_query(callback_query_id=call.id)
			bot.send_message(self.user.message.chat.id, 'После запуска бота вашим другом вы получите уведомление!\n'
														'Ссылка для приглашения: https://t.me/fricibot?start='+self.user.ref_code)
		elif call.data == 'sale_confirm_rules':
			db.set_sale_rules(self.user.message.chat.id)
			bot.delete_message(call.message.chat.id, call.message.message_id)
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='✅ Вы приняли соглашение. Теперь можно продать что-то!').wait()
		elif call.data == 'enter_coupon_code':
			bot.answer_callback_query(callback_query_id=call.id)
			bot.send_message(self.user.message.chat.id, 'Введите код купона:', reply_markup=types.ForceReply())
	def Think(self):
		logger.info('{} - главная страница, думать - {}'.format(self.user.message.chat.id, self.user.message.text))
		if self.user.message.reply_to_message.text == 'Введите код купона:':
			result = db.activate_coupon(self.user.message.chat.id, self.user.message.text)
			text = ''
			if result == None:
				text = 'Такого купона нет!'
			elif result == False:
				text = 'Упс, кто-то уже активировал этот купон'
			elif result == True:
				text = 'Купон был успешно активирован'
			bot.reply_to(self.user.message, text, reply_markup = Page(self.user).getMarkup())
class ShopPage():
	def __init__(self, user):
		#колхозная проверка на наличии альтернативной обработки
		#сообщения у страницы(временно)
		self.isExtended = False

		#инициализируем пользователя
		self.user = user

		#инициализация кнопок 
		#self.beerButton = 'Пиво'
		#self.vodkaButton = 'Водка'
		self.backButton = 'В главное меню'

		#лист текста кнопок(для проверки в хендлере)
		self.msgList = [self.backButton]

		#создание объекта для отображения кнопок
		self.markup = types.ReplyKeyboardMarkup(row_width=2)

		#закидываем кнопки в объект для отображения
		#self.markup.row(types.KeyboardButton(self.beerButton),
		#		 types.KeyboardButton(self.vodkaButton))
		self.markup.row(types.KeyboardButton(self.backButton))
	
	#что же будет делать кнопка при нажатии?????????
	def onPressButton(self):
		button = self.user.message.text
		logger.info('{} - в магазине нажата кнопка {}'.format(self.user.message.chat.id, emoji.demojize(button)))
		if button == self.backButton:
			#тут переход на другую страницу
			self.user.setState('main')
			
			#обновление страницы
			bot.reply_to(self.user.message, "Вы ушли в мейн", reply_markup = 
			  Page(self.user).getMarkup())
	def onCommand(self):
		command = self.user.message.text
		logger.info('{} - в магазине введена команда {}'.format(self.user.message.chat.id, command))
		if command.startswith('/buy_'): #отлов /buy
			command = command[5:] # убрать префикс
			product_id = utils.convertInt(command, reverse=True)
			product = db.get_product(product_id)
			if product['status'] == 'sale':
				if self.user.balance >= product['price']:
					markup = telebot.types.InlineKeyboardMarkup()
					markup.add(telebot.types.InlineKeyboardButton(text='❌ Отменить', callback_data='buy_cancel'))
					markup.add(telebot.types.InlineKeyboardButton(text='✅ Подтвердить', callback_data='buy_confirm_{}'.format(product_id)))
					bot.send_message(self.user.message.chat.id, 'Подвердите покупку:\n\n{}\nЦена: {} 💎'.format(product['title'], product['price']),
																reply_markup=markup)
				else:
					bot.send_message(self.user.message.chat.id, '⚠️ На вашем счету недостаточно средств')
			else:
				bot.send_message(self.user.message.chat.id, 'Упс, кто-то уже купил это!')
	def handleButtonCallback(self, call):
		logger.info('{} - магазин, колбэк кнопки {}'.format(self.user.message.chat.id, call.data))
		if call.data == 'buy_cancel':
			bot.answer_callback_query(callback_query_id=call.id)
			bot.edit_message_text('Покупка была отменена', chat_id=call.message.chat.id, message_id=call.message.message_id)
		elif call.data.startswith('buy_confirm_'):
			bot.answer_callback_query(callback_query_id=call.id)
			product_id = call.data[12:] #убрать префикс
			product = db.get_product(product_id)
			if product['status'] == 'sale' and product['seller'] != call.message.chat.id:
				if self.user.balance >= product['price']:
					db.buy_product(product_id, call.message.chat.id) # изменить товар в БД
					db.add_balance(call.message.chat.id, product['price']*-1) # забрать бабки за товар
					db.add_balance(product['seller'], product['price']) # отдать бабки за товар
					bot.delete_message(call.message.chat.id, call.message.message_id)
					photos = db.get_sale_app_photos(product_id)
					media_group = []
					for photo in photos:
						media_group.append(types.InputMediaPhoto(photo['photo']))
					bot.send_message(self.user.message.chat.id, 'Поздравляю с покупкой!\n\n'
																'Название: {}\n'
																'Описание: {}\n'.format(product['title'], product['description'])).wait()
					bot.send_media_group(self.user.message.chat.id, media_group)
				else:
					bot.send_message(self.user.message.chat.id, '⚠️ На вашем счету недостаточно средств')
			elif product['seller'] == call.message.chat.id:
				bot.send_message(self.user.message.chat.id, 'Нельзя покупать свой товар!')
			else:
				bot.send_message(self.user.message.chat.id, 'Упс, кто-то уже купил это!')

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
		logger.info('{} - саппорт, нажата кнопка {}'.format(self.user.message.chat.id, emoji.demojize(button)))
		if button == self.completeButton:
			self.user.setState('main') #переход на другую станицу

			bot.reply_to(self.user.message, "Спасибо! После рассмотрения обращения мы ответим Вам", reply_markup = 
			  Page(self.user).getMarkup())

	def Think(self):
		logger.info('{} - сообщение в саппорт - {}'.format(self.user.message.chat.id, self.user.message.text))
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
		logger.info('{} - продажа, нажата кнопка {}'.format(self.user.message.chat.id, emoji.demojize(button)))
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
			logger.info('{} - продажа, ввод названия - {}'.format(self.user.message.chat.id, emoji.demojize(self.user.message.text)))
			self.saleApp.setTitle(self.user.message.text)

			#это сообщение оповещает юзера про то что следующая обработка - это елиф ниже данного коммента
			bot.send_message(self.user.id, "Напишите описание к вашему товару")
		elif self.saleApp.description == 'None':
			logger.info('{} - продажа, ввод описания - {}'.format(self.user.message.chat.id, emoji.demojize(self.user.message.text)))
			self.saleApp.setDesc(self.user.message.text)
			bot.send_message(self.user.id, "Отправьте фотографии товара (все одним сообщением)")
		elif not self.saleApp.photos or self.user.message.content_type == 'photo':
			logger.info('{} - продажа, приемка картинок'.format(self.user.message.chat.id))
			fileID = self.user.message.photo[-1].file_id
			file = bot.get_file(fileID).wait()
			pic = bot.download_file(file.file_path).wait()
			if self.user.message.media_group_id:
				if db.check_photo_media_group(self.user.message.media_group_id):
					self.saleApp.addPhoto(pic, self.user.message.media_group_id)
				else:
					self.saleApp.addPhoto(pic, self.user.message.media_group_id)
					bot.send_message(self.user.id, "Напишите цену вашего товара")
			else:
				self.saleApp.addPhoto(pic, 0)
				bot.send_message(self.user.id, "Напишите цену вашего товара")
		elif not self.saleApp.price:
			logger.info('{} - продажа, ввод цены - {}'.format(self.user.message.chat.id, emoji.demojize(self.user.message.text)))
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
		elif self.__isCommand(self.user.message):
			self.page.onCommand()
			#новая проверка,  может ли страница обрабатывать что-то кроме кнопки
		elif self.page.isExtended:
			self.page.Think()

	def handleButtonCallback(self, call):
		self.page.handleButtonCallback(call)

			#проверка на наличие кнопки
	def __isButton(self, message):
		if any(item in message.text for item in self.page.msgList):
			return True
		else:
			return False

	def __isCommand(self, message):
		if message.text[0] == '/':
			return True
		else:
			return False
