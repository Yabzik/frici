import logging
import telebot
import utils
import msg
import db

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
			  Page(db.get_user(message.chat.id)['state']).getMarkup())



@bot.message_handler()
@utils.safe
#def handle_common(message):
#	if message.text == msg.personal:
#		bot.reply_to(message, 'personal')
#	elif message.text == msg.buy:
#		db.add_balance(message.chat.id, 25)
#		pass
#	elif message.text == msg.sell:
#		pass
#	elif message.text == msg.info:
#		bot.send_message(message.chat.id, '{} \n {}'.format(msg.info_text, db.get_user_balance(message.chat.id)))
#	elif message.text == msg.support:
#		pass
def handle_common(message):
	#создавать страницы меню в menu.py
	curPage = Page(db.get_user(message.chat.id)['state'])

	if curPage.isValidMessage(message):
		curPage.pressButton(message)
	elif curPage.page_name == 'support': # отлавливаем сообщения в поддержку
		bot.reply_to(message, 'Тут должна быть обработка') #todo


# ---HANDLERS---


@utils.safe
def main():
	#db.add_user(152221)
	#db.get_user(152221)
	bot.polling()
main()

""" TODO:
report exceptions to tg


"""