import pymysql
from pymysql.cursors import DictCursor
from contextlib import closing

from utils import genRef

from conf import db_conf

def add_user(user_id, ref_id=None):
	with closing(pymysql.connect(**db_conf)) as conn:
		with conn.cursor() as cursor:
			sql = 'INSERT INTO users (user_id, balance, invited_by, ref_code, state) VALUES (%s, %s, %s, %s, %s)'
			ref_code = genRef()
			bal = 0
			state = 'main'
			if ref_id:
				bal += 25
			cursor.execute(sql, (user_id, bal, ref_id, ref_code, state))
			conn.commit()

def get_user(user_id):
	with closing(pymysql.connect(**db_conf)) as conn:
		with conn.cursor() as cursor:
			sql = 'SELECT * FROM users WHERE user_id = %s'
			cursor.execute(sql, user_id)
			return cursor.fetchone()

def get_id_by_ref(ref):
	with closing(pymysql.connect(**db_conf)) as conn:
		with conn.cursor() as cursor:
			sql = 'SELECT * FROM users WHERE ref_code = %s'
			cursor.execute(sql, ref)
			try:
				return cursor.fetchone()['user_id']
			except TypeError:
				return None

def add_balance(user_id, amount):
	with closing(pymysql.connect(**db_conf)) as conn:
		with conn.cursor() as cursor:
			sql = 'UPDATE users SET balance = balance + %s WHERE user_id = %s'
			cursor.execute(sql, (amount, user_id))
			conn.commit()

def change_state(user_id, state):
	with closing(pymysql.connect(**db_conf)) as conn:
		with conn.cursor() as cursor:
			sql = 'UPDATE users SET state = %s WHERE user_id = %s'
			cursor.execute(sql, (state, user_id))
			conn.commit()

def open_support(user_id):
	with closing(pymysql.connect(**db_conf)) as conn:
		with conn.cursor() as cursor:
			sql = 'UPDATE users SET support_state = "open" WHERE user_id = %s'
			res = cursor.execute(sql, (user_id))
			conn.commit()

def send_to_support(user_id, message):
	with closing(pymysql.connect(**db_conf)) as conn:
		with conn.cursor() as cursor:
			sql = 'INSERT INTO messages (sender, recipient, message) VALUES (%s, %s, %s)'
			res = cursor.execute(sql, (user_id, 0, message))
			conn.commit()

def get_sale_app(user_id):
	with closing(pymysql.connect(**db_conf)) as conn:
		with conn.cursor() as cursor:
			sql = 'SELECT * FROM goods WHERE seller = %s AND status = %s'
			cursor.execute(sql, (user_id, 'writing'))
			try:
				return cursor.fetchone()
			except TypeError:
				return None

def add_sale_app(user_id):
	with closing(pymysql.connect(**db_conf)) as conn:
		with conn.cursor() as cursor:
			sql = 'INSERT INTO goods (title, description, seller, status) VALUES (%s, %s, %s, %s)'
			cursor.execute(sql, ('None', 'None', user_id, 'writing'))
			conn.commit()

def add_sale_app_title(id, title):
	with closing(pymysql.connect(**db_conf)) as conn:
		with conn.cursor() as cursor:
			sql = 'UPDATE goods SET title = %s WHERE id = %s'
			cursor.execute(sql, (title, id))
			conn.commit()

def add_sale_app_desc(id, desc):
	with closing(pymysql.connect(**db_conf)) as conn:
		with conn.cursor() as cursor:
			sql = 'UPDATE goods SET description = %s WHERE id = %s'
			cursor.execute(sql, (desc, id))
			conn.commit()

def add_sale_app_price(id, price):
	with closing(pymysql.connect(**db_conf)) as conn:
		with conn.cursor() as cursor:
			sql = 'UPDATE goods SET price = %s WHERE id = %s'
			cursor.execute(sql, (price, id))
			conn.commit()

def set_sale_app_status(id, status):
	with closing(pymysql.connect(**db_conf)) as conn:
		with conn.cursor() as cursor:
			sql = 'UPDATE goods SET status = %s WHERE id = %s'
			cursor.execute(sql, (status, id))
			conn.commit()

def del_sale_app(id):
	with closing(pymysql.connect(**db_conf)) as conn:
		with conn.cursor() as cursor:
			sql = 'DELETE FROM goods WHERE id = %s;'
			cursor.execute(sql, id)
			conn.commit()