#create a command line interface for the application
import sqlite3

class User():
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
CONNECTION_STRING = 'fantasy_league.db'
USER = User("", "", "")

def print_table(headers, data):
    # Print the header row
    header_row = ""
    for header in headers:
        header_row += f"{header:<15}"
    
    print(header_row)
    print("-" * len(header_row))

    # Print each data row
    for row in data:
        row_str = ""
        for col in row:
            row_str += f"{str(col):<15}"
        print(row_str)

# region User Functions
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

def check_password(db, password, email):
    db.execute('''SELECT password
                FROM user
                WHERE password = ? AND email = ?''', (password, email))
    result = db.fetchone()
    return result is not None

# use email and password to login
def login(db):
    global USER
    while(True):
        email = input("Enter your email: ")
        if(check_if_email_exists(db, email) == True):
                password = input("Enter your password: ")
                if(check_password(db, password, email) == False):
                    print("Password incorrect. Please try again.")
                    return False
                else:
                    #set default USER to the stored user values in the table
                    db.execute('''SELECT * from user
                                WHERE email = ?''', (email,))
                    result = db.fetchone()
                    USER = User(result[0], result[1], result[2])

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
                break

    # team creation
    team_name = input("Enter your team name: ")
    db.execute('''INSERT INTO team (team_name, email)
                VALUES (?, ?)''', (team_name, USER.email))
    db_connection.commit()
    
    print(f"Welcome to the CLI Fantasy League, {USER.username}!")
    return True
# endregion

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

def roster_menu(db):
    while(True):
        print("===================================")
        print("1. View Roster")
        print("2. Add Player")
        print("3. Drop Player")
        print("Q. Quit")
        
        choice = input("Enter your choice: ")

        #Should return the player's names, positions, and real team that are on the selected user's team
        #players not on a team have a value of 0 in the team_id column
        if choice == "1":
            print("===================================")
            print("> Viewing Roster")
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
        #Should update the player's team_id to the selected user's team_id, if it already has a different
        #team_id, thhen it will ask the user to pick another player
        elif choice == "2":
            print("===================================")
            print("> Adding Player")
            quit = False
            while(not quit):
                player_name = input("Enter the player's name: (Q to quit) ")
                if(player_name == "Q"):
                    quit = True
                    continue
                # check if the player exists
                db.execute('''SELECT player_name
                            FROM player
                            WHERE player_name = ?''', (player_name,))
                condition = db.fetchone()
                if condition is None:
                    print("> Player not found. Please try again.")
                    continue
                #check if the player is already on a team
                db.execute('''SELECT team_id
                            FROM player
                            WHERE player_name = ?''', (player_name,))
                condition = db.fetchone()[0]
                if(condition == 0):
                    print("> Player Avaiable!")
                    #update the player relation to change their team_id to the user's team_id
                    db.execute('''
                        UPDATE player
                        SET team_id = (SELECT team_id
                                FROM team
                                WHERE team.email = ?)
                            WHERE player_name = ?''', (USER.email,player_name,))
                    db_connection.commit()
                    print(f"> {player_name} added to your team.")
                    quit = True
                else:
                    print("> Player already in a team. Select another player.")
        elif choice == "3":
            #drop player
            print("===================================")
            print("> Dropping Player")
            #Should update the player's team_id to 0, if it already has a team_id of 0, then it will ask the user to pick another player
            quit = False
            while(not quit):
                player_name = input("Enter the player's name: (Q to quit) ")
                if(player_name == "Q"):
                    quit = True
                    continue
                # check if the player exists
                db.execute('''SELECT player_name, team_id
                            FROM player
                            WHERE player_name = ?''', (player_name,))
                condition = db.fetchone()
                if condition is None:
                    print("> Player not found. Please try again.")
                    continue
                #check if the player is already on a team
                if(condition[1] == 0):
                    print("> Player already not on a team. Select another player.")
                    continue
                #check if the player is on the user's team, if not, then the cannot drop the player
                elif(condition[1] != 0):
                    db.execute('''SELECT team_id
                                FROM team
                                WHERE email = ?''', (USER.email,))
                    team_id = db.fetchone()[0]
                    if(condition[1] != team_id):
                        print("> Player not on your team. Please try again.")
                        continue
                    else:
                        quit = True
                        #update the player relation to change their team_id to 0
                        db.execute('''
                            UPDATE player
                            SET team_id = 0
                            WHERE player_name = ?''', (player_name,))
                        db_connection.commit()
                        print(f"> {player_name} dropped from your team.")
        elif choice == "Q":
            break
        else:
            print("===================================")            
            print("> Invalid choice. Please try again.")

def player_statistics(db):
    print("> Viewing Player Statistics")
    #Should return the selected player's statistics for a given week
    while(True):
        player_name = input("Enter the player's name: (Q to Quit) ")
        if player_name == "Q":
            break
        week = input("Enter the week (A to view all weeks): ")
        query = '''SELECT * 
                    FROM player_statistics
                    WHERE player_id = (SELECT player_id
                                        FROM player
                                        WHERE player_name = ?'''
        params = [player_name]
        if (week != "A"):
            # check if the week is a number
            if not week.isdigit():
                print("> Invalid week. Please try again.")
                continue
            query += " AND week = ?"
            params.append(week)
        query += ")"

        db.execute(query, params)

        results = db.fetchall()
        if len(results) == 0:
            msg = f"> No statistics found for {player_name}"
            if week != "A":
                msg += f" in Week {week}"
            print(msg)
        else:
            headers = ["Player ID", "Week", "Passing Yards", "Rushing Yards", "Passing TDs", "Rusing TDs", "Receptions", "Fumbles", "Interceptions", "Total Points", "Is Starting"]
            print_table(headers, results)

if __name__ == "__main__":
    db_connection = sqlite3.connect(CONNECTION_STRING)
    db = db_connection.cursor()
    main_menu(db)

    while(True):
        print(f"1. {USER.username}'s Roster")
        print("2. View Player Statistics")
        print("L. Logout")

        choice = input("Enter your choice: ")

        if choice == "L":
            print(f"=== Thank you for using the CLI Fantasy League, {USER.username}! ===")
            main_menu(db)
        elif choice == "1":
            roster_menu(db)
        elif choice == "2":
            player_statistics(db)
        else:
            print("> Invalid choice. Please try again.")