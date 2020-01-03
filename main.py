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


bot = telebot.AsyncTeleBot("605894746:AAHprnzygPIMD0yBCeecyC0kYehYKBWoOQ0")
# ---INIT---


# ---HANDLERS---
@utils.safe
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	if not db.get_user(message.chat.id): # if new user
		if len(message.text.split()) > 1: # if referal in /start
			refid = db.get_id_by_ref(message.text.split()[1])
			if refid: # if refid is not none
				db.add_user(message.chat.id, ref_id=refid)
				db.add_balance(refid, 25)
			else:
				db.add_user(message.chat.id)
		else:
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


# ---HANDLERS---


@utils.safe
def main():
	bot.polling()
main()
