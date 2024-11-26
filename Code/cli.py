#create a command line interface for the application
import sqlite3

CONNECTION_STRING = 'fantasy_league.db'

def login(db):
    print("Login failed. Please try again.")
    return False

def register(db):
    return True

if __name__ == "__main__":
    db_connection = sqlite3.connect(CONNECTION_STRING)
    db = db_connection.cursor()
    
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

        print("Welcome to the CLI Fantasy League!")
    
    db_connection.close()

