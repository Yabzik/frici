import logging
import msg

logger = logging.getLogger('frici')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('error.log')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(file_handler)

def safe(func):
    def func_wrapper(*args, **kwargs):
        try:
           return func(*args, **kwargs)
        except Exception as e:
            logger.error(e, exc_info=True)
            return None
    return func_wrapper


def genMarkup(type):
	from telebot import types
	# Using the ReplyKeyboardMarkup class
	# It's constructor can take the following optional arguments:
	# - resize_keyboard: True/False (default False)
	# - one_time_keyboard: True/False (default False)
	# - selective: True/False (default False)
	# - row_width: integer (default 3)
	# row_width is used in combination with the add() function.
	# It defines how many buttons are fit on each row before continuing on the next row.
	if type == 'main':
		markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
		myaccountbtn = types.KeyboardButton(msg.personal)
		infobtn = types.KeyboardButton(msg.info)
		buybtn = types.KeyboardButton(msg.buy)
		sellbtn = types.KeyboardButton(msg.sell)
		suppbtn = types.KeyboardButton(msg.support)
		markup.row(myaccountbtn)
		markup.row(buybtn, sellbtn)
		markup.row(infobtn)
		markup.row(suppbtn)
		return markup

def checkCommon(message):
	common = [msg.personal, msg.info, msg.buy, msg.sell, msg.support]
	if any(comm in message.text for comm in common):
		return True
	else:
		return False

def genRef():
	import random, string
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def convertInt(inp, reverse=False):
	orig_hex = '0123456789abcdef'
	custom_hex = 'qdvbhukmrzilycna'
	trns = str.maketrans(orig_hex, custom_hex)
	rev_trns = str.maketrans(custom_hex, orig_hex)
	if reverse:
		return int(inp.translate(rev_trns), 16)
	else:
		return hex(inp)[2:].translate(trns)

status = {
	'checking': 'проверяется',
	'sale': 'в продаже',
	'sold': 'продано',
	'declined': 'отклонено'
}