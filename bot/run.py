from email import message
import telebot 			# Telegram API |pip install pyTelegramBotAPI
from telebot import types	
import keyboard as kb
bot = telebot.TeleBot('5191831545:AAFFNCN82WjntG-29Yg5AMQq3A0a1NSdHhY')
import db
import blacklist
admin_id = 567020315
# admin_id = 479555787




# @bot.message_handler(func=lambda message: str(message.chat.id) not in db.get_users())	# Если пользователя нет в списке
# def auth(message):
# 	"""Авторизация, будет отсеивать всех , кого нет в списке пользователей"""

# 	bot.send_message(message.chat.id, "Вы не зарегестрированы, без регистрации использование сервиса невозможно") # Отправляем ему сообщение
# 	msg = f"""Новый пользователь хочет зарегистрироваться
# user_id ::: {message.chat.id} 
# first_name ::: {message.from_user.first_name}
# username ::: {message.from_user.username}
# last_name ::: {message.from_user.last_name}
# Сообщение ::: {message.text}"""
# 	bot.send_message(admin_id, msg, reply_markup=kb.new_user_need_register_kb()) #, reply_markup = keyboard.register_key(message.from_user.id))


# @bot.callback_query_handler(func=lambda call:  call.data == 'refuse_registration')
# def refuse_registration(call):
# 	for line in call.message.text.splitlines():
# 		if 'username' in line : username = line.split(':::')[1].strip()
# 		elif 'first_name' in line : first_name = line.split(':::')[1].strip()
# 		# elif 'user_id' in line : user_id = line.split(':::')[1].strip()
# 		# elif 'last_name' in line : last_name = line.split(':::')[1].strip()
# 		# elif 'Сообщение' in line : Сообщение = line.split(':::')[1].strip()
# 	if username and username != 'None': user = username
# 	elif first_name and first_name != 'None': user = first_name

# 	msg = f"""Пользователю {user} отказано в регистрации """
# 	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, reply_markup=None)




# @bot.callback_query_handler(func=lambda call:  call.data == 'confirm_registration')
# def confirm_registration(call):

# 	for line in call.message.text.splitlines():
# 		if 'user_id' in line : 
# 			user_id = line.split(':::')[1].strip()
	
# 	if db.check_user_exist(user_id):
# 		bot.send_message(admin_id, text=f"Пользователь {user_id} уже зарегестрирован")
# 	else:
# 		db.add_users(user_id)
# 		bot.send_message(admin_id, text=f'Пользователь  {user_id} успешно зарегестрирован')

########################################################################################################################################################################################################################################################
@bot.callback_query_handler(func=lambda message:  message.text == 'Главное меню')
def main_menu(message):
	msg = 'Что делать?'
	bot.send_message(message.chat.id, msg, reply_markup=kb.main_menu())


################### Добавление

@bot.message_handler(func=lambda message:  message.text == 'Добавить номер')
def block_step1(message):
	msg = 'Отправьте номер телефона'
	sent = bot.send_message(message.chat.id, msg, reply_markup=kb.return_to_main()) 
	bot.register_next_step_handler(sent, get_number) 

def get_number(message):
	if message.text == "Главное меню": 
		main_menu(message)
		return

	phone = message.text
	msg = 'Укажите причину блокировки'
	sent = bot.send_message(message.chat.id, msg, reply_markup=kb.return_to_main()) 
	bot.register_next_step_handler(sent, get_description, phone) 

def get_description(message, phone):
	if message.text == "Главное меню": 
		main_menu(message)
		return

	description = message.text
	phones = blacklist.format_phone(phone)
	try:
		for phone in phones:
			blacklist.add(phone, description)
		msg = f'Номера {phones[0]} и {phones[1]} заблокированы по причине: {description}'
		bot.send_message(message.chat.id, msg, reply_markup=kb.main_menu()) 
	except:
		msg = f'Номера {phones[0]} и {phones[1]} не заблокированы, при блокировке произошла ошибка'

		bot.send_message(message.chat.id, msg, reply_markup=kb.main_menu()) 


################ Удаление
@bot.message_handler(func=lambda message:  message.text == 'Удалить номер')
def unblock_step1(message):
	msg = 'Отправьте номер телефона'
	sent = bot.send_message(message.chat.id, msg, reply_markup=kb.return_to_main()) 
	bot.register_next_step_handler(sent, unblock) 

def unblock(message):
	if message.text == "Главное меню": 
		main_menu(message)
		return
	phone = message.text
	phones = blacklist.format_phone(phone)
	try:
		for phone in phones:
			blacklist.del_in_black_list(phone)
		msg = f'Номера {phones[0]} и {phones[1]} удалены из черного списка'
		bot.send_message(message.chat.id, msg, reply_markup=kb.main_menu()) 
	except Exception as er:
		print(er)
		msg = f'Номера {phones[0]} и {phones[1]} не удалены, при удалении произошла ошибка'

		bot.send_message(message.chat.id, msg, reply_markup=kb.main_menu()) 

@bot.message_handler()	
def main(message):
	msg = 'Что делать?'
	bot.send_message(message.chat.id, msg, reply_markup=kb.main_menu())
########################################################################################################################################################################################################################################################

bot.polling()
