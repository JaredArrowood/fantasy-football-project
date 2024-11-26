#create a command line interface for the application
import sqlite3

CONNECTION_STRING = 'fantasy_league.db'
USER = ""

def login(db):
    global USER
    USER = input("Enter your username: ")
    return True

def register(db):
    global USER
    USER = input("Enter your username: ")
    return True

# displays the login/signup portion of the CLI
def main_menu(db):
    login_success = False

    while(login_success != True):
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            login_success = login(db)
            if not login_success:
                continue
        elif choice == "2":
            login_success = register(db)    
            if not login_success:
                continue
        elif choice == "3":
            db_connection.close()
            exit()
        else:
            print("Invalid choice. Please try again.")
            continue

        print(f"=== Welcome to the CLI Fantasy League, {USER}! ===")

if __name__ == "__main__":
    db_connection = sqlite3.connect(CONNECTION_STRING)
    db = db_connection.cursor()
    main_menu(db)

    while(True):
        print("4. Logout")
        choice = input("Enter your choice: ")

        if choice == "4":
            print(f"=== Thank you for using the CLI Fantasy League, {USER}! ===")
            main_menu(db)
        else:
            print("Invalid choice. Please try again.")
