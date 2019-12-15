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