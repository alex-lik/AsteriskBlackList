from sys import argv
import sys
sys.path.insert(0, 'bot')
import blacklist


if __name__ == "__main__":
	if len(argv) < 2:
		print("Использование: python black_del.py <телефон>")
		sys.exit(1)

	phone = argv[1]

	normalized = blacklist.normalize_phone(phone)
	if not normalized:
		print(f"Неверный формат номера: {phone}")
		sys.exit(1)

	blacklist.del_in_black_list(normalized)
	print(f"Номер {normalized} удалён из черного списка")
