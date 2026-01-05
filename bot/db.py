import sqlite3
from icecream import ic
import os
dir = os.path.abspath(os.curdir)
from loguru import logger 														# Импорт логгера				#
file_name = 'log'																# Часть имени файла				#
log_file = f'{file_name}.log'	 									# Имя лог файла					#
log_format = "[{time}] [{level}] [{message}]"									# Формат лог файла  			#
logger.add(log_file, format=log_format, rotation="1 week", compression="zip")	#  Конфигурируем логгер			#
#################################################################################################################

def get_con():
	""" Подключение """
	conn = sqlite3.connect("users.db") # или :memory: чтобы сохранить в RAM
	cursor = conn.cursor()
	return conn, cursor

def create_table():
	''' Создание таблицы и индекса'''
	conn, cursor = get_con()
	cursor.execute("""CREATE TABLE users (
	id      INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id         UNIQUE
);


""")
	# cursor.execute('CREATE UNIQUE INDEX "" ON soz_auth_setting (user_id);')
	conn.commit()
	cursor.close()
	conn.close()

def select(sql):
	conn, cursor = get_con()
	cursor.execute(sql)
	result = cursor.fetchall()
	cursor.close()
	conn.close()
	return result

def insert(sql):
	conn, cursor = get_con()
	cursor.execute(sql)
	conn.commit()
	cursor.close()

def add_users(user_id):
	''' Регистрация нового пользователя '''
	try:
		sql = "insert into users (user_id) values ('%s')" % (user_id)
		insert(sql)
	except:
		print('пользователь уже добавлен')
		
def check_user_exist(user_id):
	sql = "select user_id from users where user_id = %s" % (user_id)
	if len(select(sql)) > 0: return True
	else: return None
		

def get_users():
	sql = 'select user_id from users'
	results = select(sql)
	users = []
	for result in results:
		users.append(result[0])
	return users

if __name__ == '__main__':
	try:
		create_table()
	except Exception as er:
		print(er)
	a = get_users()
	print(a)
