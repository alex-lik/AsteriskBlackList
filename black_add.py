"""Add a phone number to the Asterisk blacklist."""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot"))

import blacklist


def main() -> int:
    parser = argparse.ArgumentParser(description="Добавить номер в черный список")
    parser.add_argument("phone", help="Номер телефона")
    parser.add_argument("comment", help="Причина блокировки")
    args = parser.parse_args()

    success, message = blacklist.add(args.phone, args.comment)
    print(message)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
