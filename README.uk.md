[English](README.md) | [Русский](README.ru.md) | **Українська** | [Deutsch](README.de.md)

# AsteriskBlackList

Керування чорним списком номерів для Asterisk PBX через Telegram-бота,
веб-інтерфейс та CLI-утиліти.

## Можливості

- Додавання, видалення та перегляд заблокованих номерів
- Три інтерфейси: Telegram-бот, Flask вебзастосунок, консольні скрипти
- Нормалізація номерів до формату `+380XXXXXXXXX`
- Перевірка дублікатів перед додаванням
- Параметризовані SQL-запити, виклики Asterisk без shell

## Структура проєкту

```text
common/            спільний код (нормалізація номерів)
bot/               Telegram-бот
  run.py           точка входу, діалоги додавання/видалення
  blacklist.py     операції з AstDB через `asterisk -rx`
  keyboard.py      reply-клавіатури
web/               Flask веб-інтерфейс
  run.py           маршрути CRUD
  db.py            операції з таблицею `blacklist` у MySQL
  templates/       Jinja2-шаблони
  static/          стилі
black_add.py       CLI: додати номер
black_del.py       CLI: видалити номер
black_show.py      CLI: показати список
deploy/            systemd-юніти для деплою
```

## Вимоги

- Python 3.10+
- Asterisk з доступом до `asterisk -rx`
- MySQL з таблицею `blacklist` (для веб-інтерфейсу):

```sql
CREATE TABLE blacklist (
  phone VARCHAR(16) PRIMARY KEY,
  description VARCHAR(255)
);
```

```bash
pip install -r requirements.txt
```

## Налаштування

```bash
cp .env.example .env
```

| Змінна              | Призначення                                 |
| ------------------- | ------------------------------------------- |
| `TELEGRAM_BOT_TOKEN`| токен Telegram-бота                         |
| `ADMIN_IDS`         | ID адміністраторів через кому (порожньо — доступ усім) |
| `MYSQL_HOST/PORT/USER/PASSWORD/DB` | підключення до MySQL          |
| `WEB_HOST/PORT/DEBUG` | параметри Flask-застосунку                |
| `ASTERISK_BIN`      | шлях до бінарника `asterisk`                |

## Запуск

```bash
# Telegram-бот
python bot/run.py

# Веб-інтерфейс
python web/run.py

# CLI
python black_add.py <телефон> <коментар>
python black_del.py <телефон>
python black_show.py
```

## Як це працює

Бот керує списком через внутрішню базу Asterisk (AstDB):

```bash
asterisk -rx 'database put blacklist <номер> "<причина>"'
asterisk -rx 'database del blacklist <номер>'
asterisk -rx 'database show blacklist'
```

Веб-інтерфейс зберігає ті самі номери в MySQL-таблиці `blacklist`.
Вхідні формати (`0999999999`, `80999999999`, `380999999999`, …)
зводяться до `+380XXXXXXXXX` функцією `common.phone.normalize_phone`.

## Деплой

Готові юніти лежать у `deploy/`. Перед увімкненням виправте шляхи,
користувача та покладіть `.env` поруч із кодом:

```bash
sudo cp deploy/blacklist-bot.service deploy/blacklist-web.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now blacklist-bot blacklist-web
```
