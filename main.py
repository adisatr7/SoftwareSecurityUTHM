import os
import sqlite3


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def database_setup():
    print(f"Creating table addresses...")
    database = sqlite3.connect("sofsec_demo.db")
    cursor = database.cursor()
    cursor.execute(f"CREATE TABLE Users (  "
                    "id INT PRIMARY KEY,   "
                    "username VARCHAR(32), "
                    "password VARCHAR(32) )")
    database.commit()
    database.close()


def database_push(username, password):
    is_first_run = not os.path.isfile("sofsec_demo.db")

    database = sqlite3.connect("sofsec_demo.db")
    cursor = database.cursor()

    if is_first_run:
        database_setup()

    cursor.execute("INSERT INTO Users VALUES ("
                   ":id,"
                   ":username,"
                   ":password)", {
                       "id": len(registered_users) + 1,
                       "username": username,
                       "password": password})

    database.commit()
    database.close()


def database_get():
    is_exist = os.path.isfile("sofsec_demo.db")

    database = sqlite3.connect("sofsec_demo.db")
    cursor = database.cursor()
    records = []

    if not is_exist:
        database_setup()

    else:
        cursor.execute("SELECT * FROM Users")
        records = cursor.fetchall()

    database.commit()
    database.close()

    return records


def database_delete(username):
    is_exist = os.path.isfile("sofsec_demo.db")

    database = sqlite3.connect("sofsec_demo.db")
    cursor = database.cursor()

    if not is_exist:
        database_setup()

    else:
        cursor.execute(f"DELETE FROM Users WHERE username = '{username}'")

    database.commit()
    database.close()


def login(username, password):
    for user in registered_users:
        if user[1] == username and user[2] == password:
            print("Login successful!\n")
            return True

    print("Login failed: Username or password unknown!\n")
    return False


def register(username, password):
    if len(registered_users):
        for user in registered_users:
            if user.username == username:
                print(f"{username} already exists!\n")
                return False

    registered_users.append(User(username, password))
    database_push(username, password)
    print(f"User {username} has been successfully registered!\n")
    return True


def reveal_users():
    i = 1
    for user in registered_users:
        print(f"User {i}")
        print(f"- {user[1]}")
        print(f"- ", end="")
        for j in range(len(user[2])):
            print("*", end="")
        print("\n")
        i += 1


def delete_user(username):
    for user in registered_users:
        if user[1] == username:
            registered_users.remove(user)
            database_delete(username)
            print(f"User '{username}' has been removed from our database!\n")
            return True

    print(f"Error: User '{username}' does not exist!\n")
    return False


registered_users = database_get()
logged_in = False

while not logged_in:
    print("==============")
    print("   Welcome!   ")
    print("==============")
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    nav = input("> ")
    print("")

    if nav == "1":
        print("===========")
        print("   Login   ")
        print("===========")
        username = input("Username: ")
        password = input("Password: ")
        print("")

        if login(username, password):
            logged_in = True

    elif nav == "2":
        print("==============")
        print("   Register   ")
        print("==============")
        username = input("New username: ")
        password = input("New password: ")
        register(username, password)

    elif nav == "3":
        print("Exiting program...")
        break

    else:
        print("Error: Input invalid!\n")

while logged_in:
    print("=====================")
    print("   Admin Dashboard   ")
    print("=====================")
    print("1. Reveal all registered users")
    print("2. Delete a user")
    print("3. Logout")
    nav = input("> ")
    print("")

    if nav == "1":
        reveal_users()

    elif nav == "2":
        username = input("Enter username: ")
        print("")
        delete_user(username)

    elif nav == "3":
        print("Exiting program...")
        logged_in = False

    else:
        print("Error: Input invalid!")
