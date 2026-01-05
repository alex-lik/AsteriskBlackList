# import pymysql
# class DB:
# 	host = '127.0.0.1'			# IP хоста с базой
# 	user = 'taxi'				# Логин к базе
# 	password = '123!@#qwe'      # Пароль к базе
# 	database = 'asterisk'		# База
	
# def mysql_conect():					# Функция подключения к базе
# 	connection = pymysql.connect(host=DB.host, user=DB.user, password=DB.password, db=DB.database)
# 	cursor = connection.cursor()	# Подключение
# 	return connection, cursor				# Возвращаем подключение


# def mysql_select(sql):				# Функция выполнения SELECT запросов 
# 	try:
# 		connection, cursor = mysql_conect()		# Подключение
# 		cursor.execute(sql)				# Выполняем запрос
# 		results = cursor.fetchall()		# Получаем результат 
# 		connection.close()				# Закрываем соединение
# 	finally:
# 		return results					# Возвращаем результат


# def mysql_update(sql):
# 	try:
# 		connection, cursor = mysql_conect()		# Подключение
# 		cursor.execute(sql)
# 		connection.commit()
# 	finally:
# 		connection.close()
		

# def get_blacklist():
# 	sql = "select phone, description from blacklist"
# 	result = mysql_select(sql)
# 	data = []
# 	if len(result) > 0:
# 		for phone, description in result: data.append({'phone':phone, 'comment':description})
# 	return data

# def add_phone(phone, description):
# 	sql = f"""insert into blacklist (phone, description) values ("{phone}", "{description}")"""
# 	mysql_update(sql)
		

# def del_phone(phone):
# 	sql = f"""delete from blacklist where phone = "{phone}" """
# 	mysql_update(sql)
import pymysql

class DB:
    host = '127.0.0.1'      # IP хоста с базой
    user = 'taxi'           # Логин к базе
    password = '123!@#qwe'  # Пароль к базе
    database = 'asterisk'   # База данных

def mysql_connect():
    connection = pymysql.connect(host=DB.host, user=DB.user, password=DB.password, db=DB.database)
    cursor = connection.cursor()    # Подключение
    return connection, cursor

def mysql_select(sql):
    try:
        connection, cursor = mysql_connect()    # Подключение
        cursor.execute(sql)    # Выполняем запрос
        results = cursor.fetchall()    # Получаем результат
    finally:
        connection.close()    # Закрываем соединение
        return results    # Возвращаем результат

def mysql_update(sql):
    try:
        connection, cursor = mysql_connect()    # Подключение
        cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()

def get_blacklist():
    sql = "SELECT phone, description FROM blacklist"
    result = mysql_select(sql)
    data = []
    if len(result) > 0:
        for phone, description in result:
            data.append({'phone':phone, 'comment':description})
    return data

def add_phone(phone, description):
    sql = f'INSERT INTO blacklist (phone, description) VALUES ("{phone}", "{description}")'
    mysql_update(sql)

def del_phone(phone):
    sql = f'DELETE FROM blacklist WHERE phone = "{phone}"'
    mysql_update(sql)