"""Print the Asterisk blacklist."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot"))

import blacklist


def main() -> int:
    output = blacklist.show_blacklist()
    if output is None:
        print("Не удалось получить черный список")
        return 1
    print(output, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
