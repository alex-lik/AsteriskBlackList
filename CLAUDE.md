# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Описание проекта

Система управления чёрным списком для Asterisk PBX с двумя интерфейсами: Telegram-бот и веб-приложение Flask. Позволяет добавлять, удалять и просматривать заблокированные номера телефонов.

## Запуск

```bash
# Telegram бот
python bot/run.py

# Веб-интерфейс (порт 81)
python web/run.py

# CLI утилиты
python black_add.py <телефон> <комментарий>
python black_del.py <телефон>
```

## Зависимости

```bash
pip install pyTelegramBotAPI Flask pymysql loguru icecream keyboa
```

## Архитектура

### Два независимых сервиса

1. **bot/** — Telegram-бот для администраторов
   - `run.py` — точка входа, обработка команд
   - `blacklist.py` — операции с чёрным списком через Asterisk CLI
   - `db.py` — SQLite база для авторизации пользователей
   - `keyboard.py` — клавиатуры Telegram

2. **web/** — Flask веб-интерфейс
   - `run.py` — Flask приложение, маршруты CRUD
   - `db.py` — MySQL операции с таблицей blacklist
   - `templates/` — Jinja2 шаблоны

### Работа с Asterisk

Оба сервиса управляют чёрным списком через CLI команды Asterisk:
```bash
asterisk -rx 'database put blacklist <номер> "<причина>"'
asterisk -rx 'database del blacklist <номер>'
asterisk -rx 'database show blacklist'
```

### Нормализация телефонов

Телефоны приводятся к двум форматам:
- Полный: `+380XXXXXXXXX`
- Короткий: `0XXXXXXXXX`

Логика нормализации дублируется в `bot/blacklist.py` и `web/run.py`.

## Конфигурация

- **Telegram токен**: захардкожен в `bot/run.py`
- **Admin ID**: захардкожены в `bot/run.py` (567020315, 479555787)
- **MySQL**: credentials в `web/db.py` (user='taxi', db='asterisk')

## Деплой

Используются systemd-сервисы:
- `bot/blacklist_bot.service`
- `web/blacklist.service`
