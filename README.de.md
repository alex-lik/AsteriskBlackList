[English](README.md) | [Русский](README.ru.md) | [Українська](README.uk.md) | **Deutsch**

# AsteriskBlackList

Verwaltung der Blacklist für Asterisk PBX über einen Telegram-Bot,
eine Weboberfläche und CLI-Tools.

## Funktionen

- Blockierte Nummern hinzufügen, entfernen und auflisten
- Drei Schnittstellen: Telegram-Bot, Flask-Webanwendung, Konsolenskripte
- Normalisierung der Nummern ins Format `+380XXXXXXXXX`
- Duplikatprüfung vor dem Hinzufügen
- Parametrisierte SQL-Abfragen, Asterisk-Aufrufe ohne Shell

## Projektstruktur

```text
common/            gemeinsamer Code (Nummernormalisierung)
bot/               Telegram-Bot
  run.py           Einstiegspunkt, Dialoge zum Hinzufügen/Entfernen
  blacklist.py     AstDB-Operationen via `asterisk -rx`
  keyboard.py      Reply-Tastaturen
web/               Flask-Weboberfläche
  run.py           CRUD-Routen
  db.py            Operationen mit der `blacklist`-Tabelle in MySQL
  templates/       Jinja2-Templates
  static/          Styles
black_add.py       CLI: Nummer hinzufügen
black_del.py       CLI: Nummer entfernen
black_show.py      CLI: Liste anzeigen
deploy/            systemd-Units für das Deployment
```

## Voraussetzungen

- Python 3.10+
- Asterisk mit Zugriff auf `asterisk -rx`
- MySQL mit einer `blacklist`-Tabelle (für das Webinterface):

```sql
CREATE TABLE blacklist (
  phone VARCHAR(16) PRIMARY KEY,
  description VARCHAR(255)
);
```

```bash
pip install -r requirements.txt
```

## Konfiguration

```bash
cp .env.example .env
```

| Variable            | Zweck                                        |
| ------------------- | -------------------------------------------- |
| `TELEGRAM_BOT_TOKEN`| Telegram-Bot-Token                           |
| `ADMIN_IDS`         | Admin-IDs, kommagetrennt (leer — Zugriff für alle) |
| `MYSQL_HOST/PORT/USER/PASSWORD/DB` | MySQL-Verbindung               |
| `WEB_HOST/PORT/DEBUG` | Flask-Anwendungsparameter                  |
| `ASTERISK_BIN`      | Pfad zur `asterisk`-Binärdatei               |

## Start

```bash
# Telegram-Bot
python bot/run.py

# Weboberfläche
python web/run.py

# CLI
python black_add.py <Telefonnummer> <Kommentar>
python black_del.py <Telefonnummer>
python black_show.py
```

## Funktionsweise

Der Bot verwaltet die Liste über die interne Asterisk-Datenbank (AstDB):

```bash
asterisk -rx 'database put blacklist <Nummer> "<Grund>"'
asterisk -rx 'database del blacklist <Nummer>'
asterisk -rx 'database show blacklist'
```

Das Webinterface speichert dieselben Nummern in der MySQL-Tabelle `blacklist`.
Eingehende Formate (`0999999999`, `80999999999`, `380999999999`, …)
werden von `common.phone.normalize_phone` auf `+380XXXXXXXXX` normalisiert.

## Deployment

Fertige Units liegen in `deploy/`. Vor dem Aktivieren Pfade und Benutzer
anpassen und `.env` neben den Code legen:

```bash
sudo cp deploy/blacklist-bot.service deploy/blacklist-web.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now blacklist-bot blacklist-web
```
