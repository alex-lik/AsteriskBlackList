"""Shared helpers for the Asterisk blacklist services."""

import re
from typing import Optional


def normalize_phone(phone: str) -> Optional[str]:
    """Normalize a phone number to the ``+380XXXXXXXXX`` format.

    Accepts ``+380999999999``, ``380999999999``, ``80999999999``,
    ``0999999999`` and ``999999999``. Returns ``None`` for invalid input.
    """
    if not phone:
        return None
    digits = re.sub(r"\D", "", phone)

    if len(digits) == 9:
        return "+380" + digits
    if len(digits) == 10 and digits.startswith("0"):
        return "+38" + digits
    if len(digits) == 11 and digits.startswith("80"):
        return "+3" + digits
    if len(digits) == 12 and digits.startswith("380"):
        return "+" + digits
    return None
