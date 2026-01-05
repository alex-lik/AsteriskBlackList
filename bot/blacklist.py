from os import system
import subprocess
import re

def normalize_phone(phone):
	"""
	Нормализация номера телефона к формату +380XXXXXXXXX
	Принимает: +380999999999, 380999999999, 80999999999, 0999999999, 999999999
	Возвращает: +380999999999 или None если номер невалидный
	"""
	digits = re.sub(r'\D', '', phone)

	if len(digits) == 9:
		return '+380' + digits
	elif len(digits) == 10 and digits.startswith('0'):
		return '+38' + digits
	elif len(digits) == 11 and digits.startswith('80'):
		return '+3' + digits
	elif len(digits) == 12 and digits.startswith('380'):
		return '+' + digits
	else:
		return None


def phone_exists(phone):
	"""Проверка существования номера в blacklist Asterisk"""
	normalized = normalize_phone(phone) if not phone.startswith('+380') else phone
	if not normalized:
		return False
	result = subprocess.run(
		['asterisk', '-rx', f'database show blacklist'],
		capture_output=True, text=True
	)
	return normalized in result.stdout


def format_phone(phone):
	"""
	Приведение номера к формату +380XXXXXXXXX
	Для совместимости возвращает кортеж (full_phone, short_phone)
	"""
	normalized = normalize_phone(phone)
	if not normalized:
		return None
	short_phone = '0' + normalized[4:]  # +380XXXXXXXXX -> 0XXXXXXXXX
	return normalized, short_phone


def add(phone, comment):
	"""
	Добавление номера в черный список
	Возвращает: (success: bool, message: str)
	"""
	normalized = normalize_phone(phone) if not phone.startswith('+380') else phone
	if not normalized:
		return False, "Неверный формат номера"

	if phone_exists(normalized):
		return False, f"Номер {normalized} уже в черном списке"

	comment = comment.replace(' ', '_')
	system(f"""asterisk -rx "database put blacklist {normalized} '{comment}'" """)
	print(f"""Blocked number: {normalized}. Reason for blocking:{comment}""")
	return True, f"Номер {normalized} добавлен в черный список"

def show_blacklist():
	command = f"""asterisk -rx "database show"|grep black"""
	system(command)


def del_in_black_list(phone):
	""" Удаление номера из черного списка """
	normalized = normalize_phone(phone) if not phone.startswith('+380') else phone
	if not normalized:
		return False
	system(f"""asterisk -rx "database del blacklist {normalized}" """)
	print(f"""Number {normalized} removed from the black list""")
	return True