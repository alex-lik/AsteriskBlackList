from os import system

def show_blacklist():
	command = f"""asterisk -rx "database show"|grep black"""
	system(command)


if __name__ == "__main__":
    show_blacklist()