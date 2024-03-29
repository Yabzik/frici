#prod
import logging
import telebot
import utils
import msg
import db

import flask, time

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

API_TOKEN = '605894746:AAG0WlMjuXoFtKjMOhdhRDkrA-0Ca1uC06I'

bot = telebot.AsyncTeleBot(API_TOKEN)

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
				ref_code = message.text.split()[1]
				if ref_code.isdigit() and int(ref_code) < 100: #utm метка
					main_logger.info('{} - /start - Новый пользователь, UTM - {}'.format(message.chat.id, ref_code))
					db.add_user(message.chat.id, ref_id=(int(ref_code)*-1))
				else:
					main_logger.info('{} - /start - Новый пользователь, реф невалидный - {}'.format(message.chat.id, ref_code))
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

# ---WEBHOOK---

# ЗАКОММЕНТИТЬ ПРИ РАЗРАБОТКЕ И РАСКОМЕНТИТЬ ПОЛЛИНГ

WEBHOOK_HOST = 'yabzik.online'
WEBHOOK_LISTEN = '0.0.0.0' 

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, 443)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
@utils.safe
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

bot.remove_webhook()

time.sleep(1)

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

app.run(host=WEBHOOK_LISTEN,
        port=9850,
        debug=False)

# ---WEBHOOK---

@utils.safe
def main():
	#bot.polling()
	pass
main()
