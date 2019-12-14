import logging, telebot
import utils, msg, db

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
	bot.reply_to(message, msg.hello, reply_markup=utils.genMarkup('main'))

@bot.message_handler(func=utils.checkCommon)
@utils.safe
def handle_common(message):
	if message.text == msg.personal:
		bot.reply_to(message, 'personal')
	elif message.text == msg.buy:
		pass
	elif message.text == msg.sell:
		pass
	elif message.text == msg.info:
		bot.send_message(message.chat.id, msg.info_text)
	elif message.text == msg.support:
		pass

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