#create a command line interface for the application
import sqlite3
class User():
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
    
CONNECTION_STRING = 'fantasy_league.db'
USER = User("", "", "")

def check_if_email_exists(db, email):
    db.execute('''SELECT email
                FROM user
                WHERE email = ?''', (email,)) 
    result = db.fetchone()
    return result is not None

def check_username(db, username):
    db.execute('''SELECT username
                FROM user
                WHERE username = ?''', (username,))
    result = db.fetchone()
    return result is not None

def check_password(db, password):
    db.execute('''SELECT password
                FROM user
                WHERE password = ?''', (password,))
    result = db.fetchone()
    return result is not None

# use email and password to login
def login(db):
    global USER
    while(True):
        email = input("Enter your email: ")
        if(check_if_email_exists(db, email) == True):
                password = input("Enter your password: ")
                if(check_password(db, password) == False):
                    print("Password incorrect. Please try again.")
                    return False
                else:
                    #set default USER to the stored user values in the table
                    db.execute('''SELECT username
                                FROM user
                                WHERE email = ?''', (email,))
                    USER.username = db.fetchone()[0]
                    db.execute('''SELECT password
                                FROM user
                                WHERE email = ?''', (email,))
                    USER.password = db.fetchone()[0]
                    USER.email = email
                    print(f"Welcome back, {USER.username}!")
                    break
        else:
            print("Email not found. Please try again or register an account with us!")
            return False

    return True

def register(db):
    global USER
    while(True):
        email = input("Enter your email: ")
        if(check_if_email_exists(db, email) == True):
            print("Email already exists. Please try again.")
            return False
        else:
            username = input("Enter your username: ")
            if(check_username(db, username) == True):
                print("Username already exists. Please try again.")
                return False
            else:
                password = input("Enter your password: ")
                db.execute('''INSERT INTO user (email, username, password)
                            VALUES (?, ?, ?)''', (email, username, password))
                db_connection.commit()
                USER = User(email, username, password)
                print(f"Welcome to the CLI Fantasy League, {USER.username}!")
                break
    db.execute('''INSERT INTO team (team_name, email)
                VALUES (?, ?)''', (USER.username, USER.email))
    db_connection.commit()
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
        
        print(f"=== Welcome to the CLI Fantasy League, {USER.username}! ===")

if __name__ == "__main__":
    db_connection = sqlite3.connect(CONNECTION_STRING)
    db = db_connection.cursor()
    main_menu(db)

    while(True):
        print("4. Logout")
        print("5. View Roster")
        print("6. View Player Statistics")

        choice = input("Enter your choice: ")

        if choice == "4":
            print(f"=== Thank you for using the CLI Fantasy League, {USER.username}! ===")
            main_menu(db)
        elif choice == "5":
            while(True):
                print("1. View Roster")
                print("2. Add Player")
                print("3. Drop Player")
                print("Q. Quit")
                choice = input("Enter your choice: ")
                if choice == "1":
                    print("Viewing Roster")
                    #Should return the player's names, positions, and real team that are on the selected user's team
                    #players not on a team have a value of 0 in the team_id column
                    db.execute('''WITH team_players(player_id) AS 
                            (SELECT player_id 
                            FROM team, player
                            WHERE player.team_id = team.team_id AND team.email = ?)

                                SELECT player_name, position, real_team
                                    FROM team_players, player
                                    WHERE team_players.player_id = player.player_id
                            ''', (USER.email,))
                    results = db.fetchall()
                    for row in results:
                        print(row)
                elif choice == "2":
                    print("Adding Player")
                    #Should update the player's team_id to the selected user's team_id, if it already has a different
                    #team_id, thhen it will ask the user to pick another player
                    quit = False
                    while(True):
                        player_name = input("Enter the player's name: (Q to quit)")
                        if(player_name == "Q"):
                            quit = True
                            break
                        # check if the player exists
                        db.execute('''SELECT player_name
                                    FROM player
                                    WHERE player_name = ?''', (player_name,))
                        condition = db.fetchone()
                        if condition is None:
                            print("Player not found. Please try again.")
                            continue
                        #check if the player is already on a team
                        db.execute('''SELECT team_id
                                    FROM player
                                    WHERE player_name = ?''', (player_name,))
                        condition = db.fetchone()[0]
                        if(condition == 0):
                            print("Player Avaiable!")
                            break
                        else:
                            print("Player already in a team. Select another player.")
                    if(quit):
                        break
                    else:
                        #update the player relation to change their team_id to the user's team_id
                        db.execute('''
                            UPDATE player
                            SET team_id = (SELECT team_id
                                   FROM team
                                   WHERE team.email = ?)
                                WHERE player_name = ?''', (USER.email,player_name,))
                        db_connection.commit()
                        print(f"{player_name} added to your team.")
                elif choice == "3":
                    #drop player
                    print("Dropping Player")
                    #Should update the player's team_id to 0, if it already has a team_id of 0, then it will ask the user to pick another player
                    quit = False
                    while(True):
                        player_name = input("Enter the player's name: (Q to quit)")
                        if(player_name == "Q"):
                            quit = True
                            break
                        # check if the player exists
                        db.execute('''SELECT player_name
                                    FROM player
                                    WHERE player_name = ?''', (player_name,))
                        condition = db.fetchone()
                        if condition is None:
                            print("Player not found. Please try again.")
                            continue
                        #check if the player is already on a team
                        db.execute('''SELECT team_id
                                    FROM player
                                    WHERE player_name = ?''', (player_name,))
                        condition = db.fetchone()[0]
                        #if the team_id is already 0, then they are not on a team
                        if(condition == 0):
                            print("Player already not on a team. Select another player.")
                            continue
                        #check if the player is on the user's team, if not, then the cannot drop the player
                        elif(condition != 0):
                            db.execute('''SELECT team_id
                                        FROM team
                                        WHERE email = ?''', (USER.email,))
                            team_id = db.fetchone()[0]
                            if(condition != team_id):
                                print("Player not on your team. Please try again.")
                                continue
                        if(quit):
                            break
                        else:
                            #update the player relation to change their team_id to 0
                            db.execute('''
                                UPDATE player
                                SET team_id = 0
                                WHERE player_name = ?''', (player_name,))
                            db_connection.commit()
                            print(f"{player_name} dropped from your team.")
                elif choice == "Q":
                    break
                else:
                    print("Invalid choice. Please try again.")
            

        elif choice == "6":
            print("Viewing Player Statistics")
            #Should return the selected player's statistics
            while(True):
                player_name = input("Enter the player's name: (Q to Quit)")
                if player_name == "Q":
                    break
                db.execute('''SELECT * 
                            FROM player_statistics
                            WHERE player_id = (SELECT player_id
                                                FROM player
                                                WHERE player_name = ?)''', (player_name,))
                results = db.fetchall()
                if len(results) == 0:
                    print("Player not found.")
                else:
                    for row in results:
                        print(row)
            
                
        else:
            print("Invalid choice. Please try again.")
