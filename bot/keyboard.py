"""Reply keyboards for the blacklist Telegram bot."""

from telebot import types


def main_menu() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Добавить номер")
    keyboard.row("Удалить номер")
    return keyboard


def return_to_main() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Главное меню")
    return keyboard
