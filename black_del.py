"""Remove a phone number from the Asterisk blacklist."""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot"))

import blacklist


def main() -> int:
    parser = argparse.ArgumentParser(description="Удалить номер из черного списка")
    parser.add_argument("phone", help="Номер телефона")
    args = parser.parse_args()

    normalized = blacklist.normalize_phone(args.phone)
    if not normalized:
        print(f"Неверный формат номера: {args.phone}")
        return 1

    if blacklist.remove(normalized):
        print(f"Номер {normalized} удалён из черного списка")
        return 0
    print(f"Номер {normalized} не удалён, произошла ошибка")
    return 1


if __name__ == "__main__":
    sys.exit(main())
