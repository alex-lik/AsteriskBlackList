**English** | [Русский](README.ru.md) | [Українська](README.uk.md) | [Deutsch](README.de.md)

# AsteriskBlackList

Manage the Asterisk PBX blacklist via a Telegram bot, web interface and CLI tools.

## Features

- Add, remove and list blocked numbers
- Three interfaces: Telegram bot, Flask web app, console scripts
- Phone normalization to the `+380XXXXXXXXX` format
- Duplicate check before adding
- Parameterized SQL queries, shell-free Asterisk calls

## Project layout

```text
common/            shared code (phone normalization)
bot/               Telegram bot
  run.py           entry point, add/remove dialogs
  blacklist.py     AstDB operations via `asterisk -rx`
  keyboard.py      reply keyboards
web/               Flask web interface
  run.py           CRUD routes
  db.py            operations on the `blacklist` MySQL table
  templates/       Jinja2 templates
  static/          styles
black_add.py       CLI: add a number
black_del.py       CLI: remove a number
black_show.py      CLI: show the list
deploy/            systemd units for deployment
```

## Requirements

- Python 3.10+
- Asterisk with `asterisk -rx` access
- MySQL with a `blacklist` table (for the web interface):

```sql
CREATE TABLE blacklist (
  phone VARCHAR(16) PRIMARY KEY,
  description VARCHAR(255)
);
```

```bash
pip install -r requirements.txt
```

## Configuration

```bash
cp .env.example .env
```

| Variable          | Purpose                                              |
| ----------------- | ---------------------------------------------------- |
| `TELEGRAM_BOT_TOKEN`| Telegram bot token                                |
| `ADMIN_IDS`         | Admin IDs, comma-separated (empty — everyone allowed) |
| `MYSQL_HOST/PORT/USER/PASSWORD/DB` | MySQL connection               |
| `WEB_HOST/PORT/DEBUG` | Flask app settings                              |
| `ASTERISK_BIN`      | path to the `asterisk` binary                      |

## Run

```bash
# Telegram bot
python bot/run.py

# Web interface
python web/run.py

# CLI
python black_add.py <phone> <comment>
python black_del.py <phone>
python black_show.py
```

## How it works

The bot manages the list through the internal Asterisk database (AstDB):

```bash
asterisk -rx 'database put blacklist <number> "<reason>"'
asterisk -rx 'database del blacklist <number>'
asterisk -rx 'database show blacklist'
```

The web interface stores the same numbers in the MySQL `blacklist` table.
Incoming formats (`0999999999`, `80999999999`, `380999999999`, …)
are normalized to `+380XXXXXXXXX` by `common.phone.normalize_phone`.

## Deployment

Ready-to-use units live in `deploy/`. Before enabling them, adjust the paths,
the user, and place `.env` next to the code:

```bash
sudo cp deploy/blacklist-bot.service deploy/blacklist-web.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now blacklist-bot blacklist-web
```
