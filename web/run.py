from flask import Flask, request, render_template, redirect
import os
import re
from os import system
import subprocess
import db
app = Flask(__name__)



# @app.route("/")
# def modem_state():
# 	result = os.popen("asterisk -rx 'dongle show devices'").read()
# 	data = []
# 	for line in result.splitlines():
# 		line = line.split()
# 		trunk = line[0]
# 		group = line[1]
# 		if trunk == 'ID': continue
# 		state = line[2] if line[2] != 'Not' else 'Not connect'
# 		rssi = line[3] if re.search('\d+', line[3]) else line[4]
# 		operator = line[6] if not re.search('\d+', line[6]) else line[7]
# 		dongle_model = line[7] if line[7] != 'UA' else line[8]
# 		phone = line[-1]
# 		data.append((trunk, state, rssi, operator, dongle_model, phone))
# 	return render_template('index.html', data=data)



@app.route("/blacklist", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
def black_list():
	if request.method == 'POST':
		phone = request.form.get("phone")
		comment = request.form.get("comment")
		comment = comment.replace(' ', '_')
		db.add_phone(phone, comment)

	black_list = db.get_blacklist()

	return render_template('blacklist.html', black_list=black_list)


@app.route('/delete/<phone>')
def delete(phone):
	db.del_phone(phone)
	print(f"""Number {phone} removed from the black list""")        # Выводим сообщение на экран
	return redirect('/blacklist')

 
 
@app.route("/incoming_sms")
def incoming_sms():
	return render_template('incomingsms.html')
 

@app.route("/balance")
def sim_balance():
	return render_template('balance.html')
 

def format_phone_number(phone_number):
	# Убираем все символы, кроме цифр
	phone_number = ''.join(filter(str.isdigit, phone_number))
	# Если номер длинее 10 символов, то отсекаем лишние цифры
	if len(phone_number) > 10:
		phone_number = phone_number[-10:]
	# Если номер начинается с 8, то заменяем на 0
	if phone_number.startswith('8'):
		phone_number = '0' + phone_number[1:]
	# Если номер начинается с +380, то заменяем на 0
	if phone_number.startswith('380'):
		phone_number = '0' + phone_number[3:]
	# Если номер начинается с 380, то заменяем на 0
	if phone_number.startswith('380'):
		phone_number = '0' + phone_number[2:]
	# Если номер начинается с 0, то оставляем без изменений
	if phone_number.startswith('0'):
		pass
	# Если номер начинается с других цифр, то добавляем 0 в начале
	else:
		phone_number = '0' + phone_number
	# Форматируем номер в виде 0XXXXXXXXX
	formatted_phone_number = f"{phone_number[:1]}{phone_number[1:4]}{phone_number[4:7]}{phone_number[7:]}"
	return formatted_phone_number
def format_phone(phone):
	""" Приведение номера телефона к формату 0ХХ-ХХХ-ХХ-ХХ и +380ХХ-ХХХ-ХХ-ХХ"""
	phone = re.sub("\D", "", phone)

	if len(phone) == 9:									# Если длина номера 9 символов 				
		phone = '0' + str(phone)						# Добавляем 0 к номеру
	elif len(phone) == 10 and phone[0] == '0': 			# Если длина номера 10 символов и первый символ 0
		phone = phone					# Добавляем к полному номеру +38, а номер оставляем без изменений
	elif len(phone) == 11 and phone[0] == '8': 			# Если длина номера 11 символов и первый символ 8
		phone = phone[1:]								# Удаляем первый символ в номере
	elif len(phone) == 12 and phone[0] == '3': 			# Если длина номера 12 символов и первый символ 3
		phone = phone[2:]								# Удаляем первые 2 символа в номере
	elif len(phone) == 13 and phone[0] == '+':			# Если длина номера 13 символов и первый символ +
		phone = phone[3:]								# Удаляем первые 3 символа в номере
	else: 												# Если как то по другому
		return None										# Ничего не возвращаем
	return phone			


if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True, port=81)
