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
        print("5. View Roster")
        print("6. View Player Statistics")

        choice = input("Enter your choice: ")

        if choice == "4":
            print(f"=== Thank you for using the CLI Fantasy League, {USER}! ===")
            main_menu(db)
        elif choice == "5":
            while(True):
                print("1. View Roster")
                print("2. Add Player")
                print("3. Drop Player")
                choice = input("Enter your choice: ")
                if choice == "1":
                    print("Viewing Roster")
                    db.execute('''WITH team_players(player_id) AS 
                            (SELECT player_id 
                            FROM team, player, user
                            WHERE player.team_id = team.team_id AND team.email = user.email)

                                SELECT player_name, position, real_team
                                    FROM team_players, player
                                    WHERE team_players.player_id = player.player_id
                            ''')
                    results = db.fetchall()
                    for row in results:
                        print(row)
                elif choice == "2":
                    print("Adding Player")
                    quit = False
                    while(True):
                        player_name = input("Enter the player's name: (Q to quit)")
                        if(player_name == "Q"):
                            quit = True
                            break
                        #check if the player is already on a team
                        db.execute('''SELECT team_id
                                    FROM player
                                    WHERE player_name = ?''', (player_name,))
                        condition = db.fetchone()
                        if(condition == None):
                            print("Player Avaiable!")
                            break
                        else:
                            print("Player already in a team. Select another player.")
                    if(quit):
                        continue
                    else:
                        db.execute('''
                            UPDATE player
                            SET team_id = (SELECT team_id
                                            FROM team, user, player
                                            WHERE team.email = user.email AND player.player_name = ?)''', (player_name,))
                        db_connection.commit()
                        print(f"{player_name} added to your team.")
            

        elif choice == "6":
            print("Viewing Player Statistics")

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
