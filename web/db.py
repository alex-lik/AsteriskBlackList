"""MySQL storage for the blacklist web interface."""

import os
import sys
from typing import List, Optional, Tuple

import pymysql

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.phone import normalize_phone


def _db_config() -> dict:
    return {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", ""),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "db": os.getenv("MYSQL_DB", "asterisk"),
        "charset": "utf8mb4",
    }


def _connect():
    return pymysql.connect(**_db_config())


def get_blacklist() -> List[dict]:
    with _connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT phone, description FROM blacklist")
            return [
                {"phone": phone, "comment": description}
                for phone, description in cursor.fetchall()
            ]


def phone_exists(phone: str) -> bool:
    normalized = normalize_phone(phone)
    if not normalized:
        return False
    with _connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM blacklist WHERE phone = %s", (normalized,)
            )
            row = cursor.fetchone()
            return row is not None and row[0] > 0


def add_phone(phone: str, description: str) -> Tuple[bool, str, Optional[str]]:
    """Add a number to the blacklist.

    Returns (success, message, normalized_phone).
    """
    normalized = normalize_phone(phone)
    if not normalized:
        return False, "Неверный формат номера", None

    if phone_exists(normalized):
        return False, f"Номер {normalized} уже в черном списке", normalized

    with _connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO blacklist (phone, description) VALUES (%s, %s)",
                (normalized, description),
            )
        connection.commit()
    return True, f"Номер {normalized} добавлен в черный список", normalized


def del_phone(phone: str) -> None:
    normalized = normalize_phone(phone) or phone
    with _connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM blacklist WHERE phone = %s", (normalized,))
        connection.commit()
