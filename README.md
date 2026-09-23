# AsteriskBlackList

Управление чёрным списком номеров для Asterisk PBX через Telegram-бота,
веб-интерфейс и CLI-утилиты.

## Возможности

- Добавление, удаление и просмотр заблокированных номеров
- Три интерфейса: Telegram-бот, Flask веб-приложение, консольные скрипты
- Нормализация номеров к формату `+380XXXXXXXXX`
- Проверка дубликатов перед добавлением
- Параметризованные SQL-запросы, вызовы Asterisk без shell

## Структура проекта

```text
common/            общий код (нормализация номеров)
bot/               Telegram-бот
  run.py           точка входа, диалоги добавления/удаления
  blacklist.py     операции с AstDB через `asterisk -rx`
  keyboard.py      reply-клавиатуры
web/               Flask веб-интерфейс
  run.py           маршруты CRUD
  db.py            операции с таблицей `blacklist` в MySQL
  templates/       Jinja2-шаблоны
  static/          стили
black_add.py       CLI: добавить номер
black_del.py       CLI: удалить номер
black_show.py      CLI: показать список
deploy/            systemd-юниты для деплоя
```

## Требования

- Python 3.10+
- Asterisk с доступом к `asterisk -rx`
- MySQL с таблицей `blacklist` (для веб-интерфейса):

```sql
CREATE TABLE blacklist (
  phone VARCHAR(16) PRIMARY KEY,
  description VARCHAR(255)
);
```

```bash
pip install -r requirements.txt
```

## Настройка

```bash
cp .env.example .env
```

| Переменная          | Назначение                              |
| ------------------- | --------------------------------------- |
| `TELEGRAM_BOT_TOKEN`| токен Telegram-бота                     |
| `ADMIN_IDS`         | ID администраторов через запятую (пусто — доступ всем) |
| `MYSQL_HOST/PORT/USER/PASSWORD/DB` | подключение к MySQL       |
| `WEB_HOST/PORT/DEBUG` | параметры Flask-приложения            |
| `ASTERISK_BIN`      | путь к бинарю `asterisk`                |

## Запуск

```bash
# Telegram-бот
python bot/run.py

# Веб-интерфейс
python web/run.py

# CLI
python black_add.py <телефон> <комментарий>
python black_del.py <телефон>
python black_show.py
```

## Как это работает

Бот управляет списком через внутреннюю базу Asterisk (AstDB):

```bash
asterisk -rx 'database put blacklist <номер> "<причина>"'
asterisk -rx 'database del blacklist <номер>'
asterisk -rx 'database show blacklist'
```

Веб-интерфейс хранит те же номера в MySQL-таблице `blacklist`.
Входящие форматы (`0999999999`, `80999999999`, `380999999999`, …)
приводятся к `+380XXXXXXXXX` функцией `common.phone.normalize_phone`.

## Деплой

Готовые юниты лежат в `deploy/`. Перед включением поправьте пути,
пользователя и положите `.env` рядом с кодом:

```bash
sudo cp deploy/blacklist-bot.service deploy/blacklist-web.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now blacklist-bot blacklist-web
```
