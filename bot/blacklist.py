"""Operations on the Asterisk blacklist database."""

import logging
import os
import subprocess
import sys
from typing import Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.phone import normalize_phone

__all__ = ["normalize_phone", "phone_exists", "add", "remove", "show_blacklist"]

ASTERISK_BIN = os.getenv("ASTERISK_BIN", "asterisk")

logger = logging.getLogger(__name__)


def _run_asterisk(arguments: str) -> subprocess.CompletedProcess:
    """Run an Asterisk CLI command without a shell."""
    return subprocess.run(
        [ASTERISK_BIN, "-rx", arguments],
        capture_output=True,
        text=True,
    )


def phone_exists(phone: str) -> bool:
    """Check whether a number is already in the Asterisk blacklist."""
    normalized = normalize_phone(phone)
    if not normalized:
        return False
    result = _run_asterisk("database show blacklist")
    if result.returncode != 0:
        logger.error("Asterisk lookup failed: %s", result.stderr.strip())
        return False
    return normalized in result.stdout


def add(phone: str, comment: str) -> Tuple[bool, str]:
    """Add a number to the blacklist.

    Returns (success, message).
    """
    normalized = normalize_phone(phone)
    if not normalized:
        return False, "Неверный формат номера"

    if phone_exists(normalized):
        return False, f"Номер {normalized} уже в черном списке"

    value = (comment or "").strip().replace(" ", "_").replace('"', "")
    result = _run_asterisk(f'database put blacklist {normalized} "{value}"')
    if result.returncode != 0:
        logger.error("Asterisk insert failed: %s", result.stderr.strip())
        return False, f"Номер {normalized} не добавлен, произошла ошибка"

    logger.info("Blocked number: %s. Reason: %s", normalized, value)
    return True, f"Номер {normalized} добавлен в черный список"


def remove(phone: str) -> bool:
    """Remove a number from the blacklist. Returns True on success."""
    normalized = normalize_phone(phone)
    if not normalized:
        return False
    result = _run_asterisk(f"database del blacklist {normalized}")
    if result.returncode != 0:
        logger.error("Asterisk delete failed: %s", result.stderr.strip())
        return False
    logger.info("Number %s removed from the black list", normalized)
    return True


def show_blacklist() -> Optional[str]:
    """Return the raw Asterisk blacklist dump, or None on error."""
    result = _run_asterisk("database show blacklist")
    if result.returncode != 0:
        logger.error("Asterisk lookup failed: %s", result.stderr.strip())
        return None
    return result.stdout
