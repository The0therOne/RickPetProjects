# Contact Book

import sqlite3

db = sqlite3.connect('contactbook.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    name TEXT,
    surname TEXT,
    phonenumber TEXT,
    country TEXT,
    email_adress TEXT
)""")

db.commit()

def new_record():
	user_name = input('Name: ')
	user_surname = input('Surname: ')
	user_phonenumber = input('Phonenumber: ')
	user_country = input('Country: ')
	user_email = input('Email: ')

	sql.execute(f"SELECT name FROM users WHERE name = '{user_name}'")
	if sql.fetchone() is None:
	    sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (user_name, user_surname, user_phonenumber, user_country, user_email ))
	    db.commit()

	    print(f'{user_name} добавлен в записную книжку!')
	else:
	    print('Такая запись уже имеется!')

	    show_record()

def show_all_records():
	for value in sql.execute("SELECT * FROM users"):
		print(value)

def show_record():
	for value in sql.execute(f"SELECT * FROM users WHERE name = '{user_name}'"):
		print(value)


def edit_record(user_name, switch):
	if switch == "1":
		new_user_name = input("New name: ")
		sql.execute(f'UPDATE users SET name = "{new_user_name}" WHERE name = "{user_name}"')
		db.commit()
	if switch == "2":
		new_user_surname = input("New surname: ")
		sql.execute(f'UPDATE users SET surname = "{new_user_surname}" WHERE name = "{user_name}"')
		db.commit()
	if switch == "3":
		new_user_phonenumber = input("New phonenumber: ")
		sql.execute(f'UPDATE users SET phonenumber = "{new_user_phonenumber}" WHERE name = "{user_name}"')
		db.commit()
	if switch == "4":
		new_user_country = input("New country: ")
		sql.execute(f'UPDATE users SET country = "{new_user_country}" WHERE name = "{user_name}"')
		db.commit()
	if switch == "5":
		new_user_email = input("New email: ")
		sql.execute(f'UPDATE users SET email_adress = "{new_user_email}" WHERE name = "{user_name}"')
		db.commit()

def remove_record(user_name):
	sql.execute(f"DELETE FROM users WHERE name = '{user_name}'")
	db.commit()

def main():
	while True:
		main_switch = input("""What do you want to do?\n
			1 - Show all records\n
			2 - Add record\n
			3 - Edit record\n
			4 - Delete record\n
			5 - Exit\n
			""")

		if main_switch == "1":
			show_all_records()
		elif main_switch == "2":
			new_record()
		elif main_switch == "3":
			user_name = input("Which user do you want to change?\n")
			sql.execute(f"SELECT name FROM users WHERE name = '{user_name}'")
			switch = input("Which value you want edit?\n1 - name\n2 - surname\n3 - phonenumber\n4 - country\n5 - email\n")
			edit_record(user_name, switch)
		elif main_switch == "4":
			user_name = input("Which user do you want to remove?\n")
			sql.execute(f"SELECT name FROM users WHERE name = '{user_name}'")
			remove_record(user_name)
		elif main_switch == "5":
			break
		else:
			print('Wrong input!')
			continue
			

if __name__ == '__main__':
	main()