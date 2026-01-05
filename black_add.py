from sys import argv
import sys
sys.path.insert(0, 'bot')
import blacklist


if __name__ == "__main__":
	if len(argv) < 3:
		print("Использование: python black_add.py <телефон> <комментарий>")
		sys.exit(1)

	phone = argv[1]
	comment = argv[2]

	normalized = blacklist.normalize_phone(phone)
	if not normalized:
		print(f"Неверный формат номера: {phone}")
		sys.exit(1)

	success, message = blacklist.add(normalized, comment)
	print(message)
