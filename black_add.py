from os import system
from sys import argv


def format_phone(phone):
	""" Приведение номера телефона к формату 0ХХ-ХХХ-ХХ-ХХ и +380ХХ-ХХХ-ХХ-ХХ"""
	if len(phone) == 9:									# Если длина номера 9 символов 				
		phone = '0' + str(phone)						# Добавляем 0 к номеру
		full_phone = '+380' + str(phone)				# Добавляем +380 к полному номеру	
	elif len(phone) == 10 and phone[0] == '0': 			# Если длина номера 10 символов и первый символ 0
		full_phone = '+38' + str(phone)					# Добавляем к полному номеру +38, а номер оставляем без изменений
	elif len(phone) == 11 and phone[0] == '8': 			# Если длина номера 11 символов и первый символ 8
		full_phone = '+3' + str(phone)					# Добавляем к полному номеру +3
		phone = phone[1:]								# Удаляем первый символ в номере
	elif len(phone) == 12 and phone[0] == '3': 			# Если длина номера 12 символов и первый символ 3
		full_phone = '+' + str(phone)					# Добавляем к полному номеру +
		phone = phone[2:]								# Удаляем первые 2 символа в номере
	elif len(phone) == 13 and phone[0] == '+':			# Если длина номера 13 символов и первый символ +
		full_phone = phone								# Полный номер не меняем
		phone = phone[3:]								# Удаляем первые 3 символа в номере
	else: 												# Если как то по другому
		return None										# Ничего не возвращаем
	return full_phone, phone							# Возвращаем полный номер и номер телефона


def add(phone, comment):
	""" Добавление номера в черный список """
	phones = format_phone(phone)						# Получаем полный и сокращенный номера
	if phones:											# Если номера получены
		for phone in phones:							# Для каждого номера
			system(f"""asterisk -rx "database put blacklist {phone} '{comment}'" """)	# Выполняем команду занесения в черный список
			print(f"""Blocked number: {phone}. Reason for blocking:{comment}""")		# Выводим сообщение на экран
	else:												# Если не удалось получить номера в полном и сокращенном формате
		print("Ошибка при форматировании номера")		# Выводим сообщение на экран
		system(f"""asterisk -rx "database put blacklist {phone} '{comment}'" """)		# Выполняем команду занесения в черный список
		print(f"""Blocked number: {phone}. Reason for blocking:{comment}""")			# Выводим сообщение на экран

if __name__ == "__main__":
	phone = argv[1]										# Получаем номер телефона из первого аргумента
	comment = argv[2]									# Получаем причину добавления из второго аргумента
	add(phone, comment)									# Заносим в черный список

