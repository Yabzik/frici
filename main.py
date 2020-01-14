import logging
import telebot
import utils
import msg
import db

from saleApplication import SaleApp

from user import User

import menu
from menu import Page

# ---INIT---
logger = telebot.logger
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('bot.log')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(file_handler)

main_logger = logging.getLogger('Main')

bot = telebot.AsyncTeleBot("605894746:AAG0WlMjuXoFtKjMOhdhRDkrA-0Ca1uC06I")
# ---INIT---


# ---HANDLERS---
@bot.message_handler(commands=['start', 'help'])
@utils.safe
def send_welcome(message):
	main_logger.info('{} - /start'.format(message.chat.id))
	if not db.get_user(message.chat.id): # if new user
		if len(message.text.split()) > 1: # if referal in /start
			refid = db.get_id_by_ref(message.text.split()[1])
			if refid: # if refid is not none
				main_logger.info('{} - /start - Новый пользователь, реф - {}'.format(message.chat.id, refid))
				bot.send_message(refid, '🏅 Кто-то запустил бота по вашей ссылке! Вы получили +25 к балансу')
				db.add_user(message.chat.id, ref_id=refid)
				db.add_balance(refid, 25)
			else:
				main_logger.info('{} - /start - Новый пользователь, реф невалидный - {}'.format(message.chat.id, message.text.split()[1]))
				db.add_user(message.chat.id)
		else:
			main_logger.info('{} - /start - новый пользователь, без рефа'.format(message.chat.id))
			db.add_user(message.chat.id)
	bot.reply_to(message, msg.hello, reply_markup = 
			  Page(User(message)).getMarkup())



@bot.message_handler(content_types=['text', 'photo'])
@utils.safe
def handle_common(message):
	#создание страницы меню в menu.py
	user = User(message)
	curPage = Page(user)

	#обработка запроса(теперь вся обработка внутри класса Page)
	curPage.handleMessage()

@bot.callback_query_handler(func=lambda call: True)
@utils.safe
def query_handler(call):
	# отлов вызовов с кнопок
	user = User(call.message)
	curPage = Page(user)

	curPage.handleButtonCallback(call)
	#if call.data == 'add':
	#	bot.answer_callback_query(callback_query_id=call.id, text='Hello world')

# ---HANDLERS---


@utils.safe
def main():
	bot.polling()
main()
