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
import re

def normalize_phone(phone):
    """
    Нормализация номера телефона к формату +380XXXXXXXXX
    Принимает: +380999999999, 380999999999, 80999999999, 0999999999, 999999999
    Возвращает: +380999999999 или None если номер невалидный
    """
    # Убираем все кроме цифр
    digits = re.sub(r'\D', '', phone)

    if len(digits) == 9:
        # 999999999 -> +380999999999
        return '+380' + digits
    elif len(digits) == 10 and digits.startswith('0'):
        # 0999999999 -> +380999999999
        return '+38' + digits
    elif len(digits) == 11 and digits.startswith('80'):
        # 80999999999 -> +380999999999
        return '+3' + digits
    elif len(digits) == 12 and digits.startswith('380'):
        # 380999999999 -> +380999999999
        return '+' + digits
    elif len(digits) == 12 and digits.startswith('380'):
        return '+' + digits
    else:
        return None


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

def phone_exists(phone):
    """Проверка существования номера в базе"""
    normalized = normalize_phone(phone)
    if not normalized:
        return False
    sql = f'SELECT COUNT(*) FROM blacklist WHERE phone = "{normalized}"'
    result = mysql_select(sql)
    return result[0][0] > 0 if result else False


def add_phone(phone, description):
    """
    Добавление номера в черный список
    Возвращает: (success: bool, message: str, normalized_phone: str|None)
    """
    normalized = normalize_phone(phone)
    if not normalized:
        return False, "Неверный формат номера", None

    if phone_exists(normalized):
        return False, f"Номер {normalized} уже в черном списке", normalized

    sql = f'INSERT INTO blacklist (phone, description) VALUES ("{normalized}", "{description}")'
    mysql_update(sql)
    return True, f"Номер {normalized} добавлен в черный список", normalized


def del_phone(phone):
    sql = f'DELETE FROM blacklist WHERE phone = "{phone}"'
    mysql_update(sql)