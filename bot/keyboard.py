from keyboa import Keyboa  # pip install keyboa
from telebot import types															# Telegram API

def main_menu():
    kb = types.ReplyKeyboardMarkup(True, True)
    kb.row("Добавить номер")
    kb.row("Удалить номер")
    return kb


def return_to_main():
    kb = types.ReplyKeyboardMarkup(True, True)
    kb.row("Главное меню")
    return kb

def new_user_need_register_kb():
    items = []
    items.append({'Зарегистрировать':"confirm_registration"})
    items.append({"Блокировать":"refuse_registration"})
    return Keyboa(items=items, items_in_row=2).keyboard

