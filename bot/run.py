"""Telegram bot for managing the Asterisk blacklist."""

import os
import sys

import telebot

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import blacklist
import keyboard as kb

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is not set")

ADMIN_IDS = {
    admin_id.strip()
    for admin_id in os.getenv("ADMIN_IDS", "").split(",")
    if admin_id.strip()
}

bot = telebot.TeleBot(TOKEN)


def is_allowed(user_id) -> bool:
    """Return True if the user may manage the blacklist."""
    if not ADMIN_IDS:
        return True
    return str(user_id) in ADMIN_IDS


def deny_access(message) -> None:
    bot.send_message(message.chat.id, "Нет доступа.", reply_markup=kb.main_menu())


@bot.message_handler(func=lambda message: message.text == "Главное меню")
def main_menu(message):
    bot.send_message(message.chat.id, "Что делать?", reply_markup=kb.main_menu())


@bot.message_handler(func=lambda message: message.text == "Добавить номер")
def block_step1(message):
    if not is_allowed(message.from_user.id):
        deny_access(message)
        return
    sent = bot.send_message(
        message.chat.id, "Отправьте номер телефона", reply_markup=kb.return_to_main()
    )
    bot.register_next_step_handler(sent, get_number)


def get_number(message):
    if message.text == "Главное меню":
        main_menu(message)
        return

    phone = message.text
    sent = bot.send_message(
        message.chat.id, "Укажите причину блокировки", reply_markup=kb.return_to_main()
    )
    bot.register_next_step_handler(sent, get_description, phone)


def get_description(message, phone):
    if message.text == "Главное меню":
        main_menu(message)
        return

    normalized = blacklist.normalize_phone(phone)
    if not normalized:
        bot.send_message(
            message.chat.id,
            f"Неверный формат номера: {phone}",
            reply_markup=kb.main_menu(),
        )
        return

    success, msg = blacklist.add(normalized, message.text)
    bot.send_message(message.chat.id, msg, reply_markup=kb.main_menu())


@bot.message_handler(func=lambda message: message.text == "Удалить номер")
def unblock_step1(message):
    if not is_allowed(message.from_user.id):
        deny_access(message)
        return
    sent = bot.send_message(
        message.chat.id, "Отправьте номер телефона", reply_markup=kb.return_to_main()
    )
    bot.register_next_step_handler(sent, unblock)


def unblock(message):
    if message.text == "Главное меню":
        main_menu(message)
        return

    normalized = blacklist.normalize_phone(message.text)
    if not normalized:
        bot.send_message(
            message.chat.id,
            f"Неверный формат номера: {message.text}",
            reply_markup=kb.main_menu(),
        )
        return

    if blacklist.remove(normalized):
        msg = f"Номер {normalized} удалён из черного списка"
    else:
        msg = f"Номер {normalized} не удалён, произошла ошибка"
    bot.send_message(message.chat.id, msg, reply_markup=kb.main_menu())


@bot.message_handler()
def main(message):
    if not is_allowed(message.from_user.id):
        deny_access(message)
        return
    bot.send_message(message.chat.id, "Что делать?", reply_markup=kb.main_menu())


if __name__ == "__main__":
    bot.infinity_polling()
