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
    # Determine the width of each column
    col_widths = [max(len(str(item)) for item in col) for col in zip(*data, headers)]
    
    # Print the header row
    header_row = " | ".join(f"{header:<{col_widths[i]}}" for i, header in enumerate(headers))

    print(header_row)
    print("-" * len(header_row))

    # Print each data row
    for row in data:
        row_str = " | ".join(f"{str(col):<{col_widths[i]}}" for i, col in enumerate(row))
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

def find_team_players(db, email):
    db.execute('''WITH team_players(player_id, is_starting) AS 
                    (SELECT DISTINCT player.player_id, is_starting
                    FROM team, player, player_statistics
                    WHERE player.team_id = team.team_id AND team.email = ? AND player.player_id = player_statistics.player_id)

                        SELECT player_name, position, real_team, is_starting
                            FROM team_players, player
                            WHERE team_players.player_id = player.player_id''' , (email,))
    return db.fetchall()

def count_players_by_position(db, email, position):
    db.execute('''WITH team_players(player_id, is_starting) AS 
                    (SELECT DISTINCT player.player_id, is_starting
                    FROM team, player, player_statistics
                    WHERE player.team_id = team.team_id AND team.email = ? AND player.player_id = player_statistics.player_id),
                        roster_stats(player_name, position, real_team, is_starting) AS 
                            (SELECT player_name, position, real_team, is_starting
                            FROM team_players, player
                            WHERE team_players.player_id = player.player_id)
               
    SELECT COUNT(*)
    FROM roster_stats
    WHERE position = ? AND is_starting = True''', (email, position))

    result = db.fetchone()
    return result[0]
    
                   
#checks for the number of starting players in each position (Still needs Defense)
def check_starting_player_counts(db):
    print("Starting Player Counts:")
    print(f"{count_players_by_position(db, USER.email, 'QB')} QBs")
    print(f"{count_players_by_position(db, USER.email, 'RB')} RBs")
    print(f"{count_players_by_position(db, USER.email, 'WR')} WRs")
    print(f"{count_players_by_position(db, USER.email, 'TE')} TEs")
    print(f"{count_players_by_position(db, USER.email, 'K')} Ks")

    if(count_players_by_position(db, USER.email, 'QB') > 1):
        print("You may only have 1 starting QB.")
        # return False
    flex_count = count_players_by_position(db, USER.email, 'RB') + count_players_by_position(db, USER.email, 'WR') + count_players_by_position(db, USER.email, 'TE')
    if(flex_count > 6):
        print("You may only have 2 starting RBs, 2 WRs, 1TE and 1 FLX in total.")
    if(count_players_by_position(db, USER.email, 'K') > 1):
        print("You may only have 1 starting K.")
        # return False

    #check if you have too little starting players
    if(count_players_by_position(db, USER.email, 'QB') < 1):
        print("You must have 1 starting QB.")
    if(flex_count < 6):
        print("You must have 2 starting RBs, 2 WRs, 1TE and 1 FLX in total.")
        # return False
    if(count_players_by_position(db, USER.email, 'K') < 1):
        print("You must have 1 starting K.")
        # return False

    # return True
    

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
        print("===================================")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        print("===================================")
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
            print("===================================")
            print("Invalid choice. Please try again.")
            continue

def roster_menu(db):
    while(True):
        print("===================================")
        print("1. View Roster")
        print("2. Add Player")
        print("3. Drop Player")
        print("4. Change Starting Lineup")
        print("Q. Quit")
        print("===================================")
        
        choice = input("Enter your choice: ")

        #Should return the player's names, positions, and real team that are on the selected user's team
        #players not on a team have a value of 0 in the team_id column
        if choice == "1":
            print("===================================")
            print("> Viewing Roster")
            print("===================================")

            check_starting_player_counts(db)
            db.execute('''WITH team_players(player_id, is_starting) AS 
                    (SELECT DISTINCT player.player_id, is_starting
                    FROM team, player, player_statistics
                    WHERE player.team_id = team.team_id AND team.email = ? AND player.player_id = player_statistics.player_id)

                        SELECT player_name, position, real_team, is_starting
                            FROM team_players, player
                            WHERE team_players.player_id = player.player_id
                        ''', (USER.email,))
            results = db.fetchall()
            clean_results = [(*item[:-1], bool(item[-1])) for item in results] # convert 0/1 to True/False
            headers = ["Player Name", "Position", "Real Team", "Is Starting"]
            print_table(headers, clean_results)
            
        #Should update the player's team_id to the selected user's team_id, if it already has a different
        #team_id, thhen it will ask the user to pick another player
        elif choice == "2":
            print("===================================")
            print("Adding Player")
            quit = False
            while(not quit):
                player_name = input("Enter the player's name: (Q to quit) ")
                if(player_name == "Q" or player_name == "q"):
                    quit = True
                    continue
                # check if the player exists
                db.execute('''SELECT player_name
                            FROM player
                            WHERE player_name = ?''', (player_name,))
                condition = db.fetchone()
                if condition is None:
                    print("===================================")
                    print("Player not found. Please try again.")
                    continue
                #check if the player is already on a team
                db.execute('''SELECT team_id
                            FROM player
                            WHERE player_name = ?''', (player_name,))
                condition = db.fetchone()[0]
                if(condition == 0):
                    print("===================================")
                    print("Player Avaiable!")
                    #update the player relation to change their team_id to the user's team_id
                    db.execute('''
                        UPDATE player
                        SET team_id = (SELECT team_id
                                FROM team
                                WHERE team.email = ?)
                            WHERE player_name = ?''', (USER.email,player_name,))
                    db_connection.commit()
                    print("===================================")
                    print(f"{player_name} added to your team.")
                    quit = True
                else:
                    print("===================================")
                    print("Player already in a team. Select another player.")
        elif choice == "3":
            #drop player
            print("===================================")
            print("Dropping Player")
            #Should update the player's team_id to 0, if it already has a team_id of 0, then it will ask the user to pick another player
            quit = False
            while(not quit):
                player_name = input("Enter the player's name: (Q to quit) ")
                if(player_name == "Q" or player_name == "q"):
                    quit = True
                    continue
                # check if the player exists
                db.execute('''SELECT player_name, team_id
                            FROM player
                            WHERE player_name = ?''', (player_name,))
                condition = db.fetchone()
                if condition is None:
                    print("===================================")
                    print("Player not found. Please try again.")
                    continue
                #check if the player is already on a team
                if(condition[1] == 0):
                    print("===================================")
                    print("Player already not on a team. Select another player.")
                    continue
                #check if the player is on the user's team, if not, then the cannot drop the player
                elif(condition[1] != 0):
                    db.execute('''SELECT team_id
                                FROM team
                                WHERE email = ?''', (USER.email,))
                    team_id = db.fetchone()[0]
                    if(condition[1] != team_id):
                        print("===================================")
                        print("Player not on your team. Please try again.")
                        continue
                    else:
                        quit = True
                        #update the player relation to change their team_id to 0
                        db.execute('''
                            UPDATE player
                            SET team_id = 0
                            WHERE player_name = ?''', (player_name,))
                        db_connection.commit()
                        print("===================================")
                        print(f"{player_name} dropped from your team.")
        elif choice == "4":
            print("Changing Starting Lineup")
            #Should update the player's is_starting value to True or False
            #if the player is already starting, then it will ask the user to pick another player
            quit = False
            while(not quit):
                player_name = input("Enter the player's name: (Q to quit) ")
                if(player_name == "Q" or player_name == "q"):
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
                    print("> Player not on a team. Select another player.")
                    continue
                #check if the player is on the user's team, if not, then the cannot change the players status
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
                        #check if the player is already starting
                        db.execute('''SELECT is_starting
                                   FROM player_statistics
                                   WHERE player_id = (SELECT player_id
                                                      FROM player
                                                      WHERE player_name = ?)''', (player_name,))
                        is_starting = db.fetchone()[0]
                        if(is_starting == True):
                            print("> Player is already starting.")
                            bench = input("Would you like to bench them? (Y/N): ")
                            if(bench == "Y"):
                                db.execute('''
                                    UPDATE player_statistics
                                    SET is_starting = False
                                    WHERE player_id = (SELECT player_id
                                                      FROM player
                                                      WHERE player_name = ?)''', (player_name,))
                                db_connection.commit()
                                print(f"> {player_name} benched.")
                            else:
                                print("> Player not benched.")
                                continue
                        else:
                            #make sure the count of starting players is less than 9
                            db.execute('''WITH team_players(player_id, is_starting) AS 
                                        (SELECT DISTINCT player.player_id, is_starting
                                            FROM team, player, player_statistics
                                            WHERE player.team_id = team.team_id AND team.email = ? AND player.player_id = player_statistics.player_id)
                                       
                                       SELECT COUNT(*)
                                       FROM team_players
                                       WHERE is_starting = True''', (USER.email,))
                            count = db.fetchone()[0]
                            print(count)
                            if(count >= 9):
                                print("> You already have 9 players starting. Please bench a player.")
                                continue
                            else:
                                start = input(f"> {player_name} is not starting. Would you like to start them? (Y/N):")
                                if(start == "Y"):
                            
                                    db.execute('''
                                        UPDATE player_statistics
                                        SET is_starting = True
                                        WHERE player_id = (SELECT player_id
                                                        FROM player
                                                        WHERE player_name = ?)''', (player_name,))
                                    db_connection.commit()
                                    print(f"> {player_name} is now starting. You have {count + 1} players starting.")
                                else:
                                    print(f"> {player_name} is not starting.")
        elif choice == "Q" or choice == "q":
            break
        else:
            print("===================================")            
            print("> Invalid choice. Please try again.")

def player_statistics(db):
    print("===================================")
    print("Viewing Player Statistics")
    print("===================================")
    #Should return the selected player's statistics for a given week
    while(True):
        player_name = input("Enter the player's name: (Q to Quit) ")
        if player_name == "Q" or player_name == "q":
            break
        week = input("Enter the week (A to view all weeks): ")
        query = '''SELECT * 
                    FROM player_statistics
                    WHERE player_id = (SELECT player_id
                                        FROM player
                                        WHERE player_name = ?'''
        params = [player_name]
        if (week != "A" and week != "a"):
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
            if week != "A" and week != "a":
                msg += f" in Week {week}"
            print("===================================")
            print(msg)
        else:
            # displaying everything except the player_id
            rest = [result[1:] for result in results]
            headers = ["Week", "Passing Yards", "Rushing Yards", "Rec. Yards", "Passing TDs", "Rushing TDs", "Rec. TDs", "Receptions", "Fumbles", "Ints", "Total Points", "Is Starting"]
            print_table(headers, rest)

def print_matchup(matchup_data):
    """Format and print a single matchup"""
    home_team, away_team, home_points, away_points, week = matchup_data
    print("===================================")
    print(f"Week {week}")
    print(f"{home_team:<20} {home_points:>5.1f}")
    print(f"{away_team:<20} {away_points:>5.1f}")
    print("===================================")

def view_current_matchup(db):
    print("===================================")
    print("Current Week Matchup")
    print("===================================")
    
    db.execute('''
        SELECT MAX(week) FROM matchup
    ''')
    current_week = db.fetchone()[0]
    
    db.execute('''
        SELECT 
            h.team_name as home_team,
            a.team_name as away_team,
            m.home_team_points,
            m.away_team_points,
            m.week
        FROM matchup m
        JOIN team h ON m.home_team_id = h.team_id
        JOIN team a ON m.away_team_id = a.team_id
        WHERE m.week = ?
        AND (h.email = ? OR a.email = ?)
    ''', (current_week, USER.email, USER.email))
    
    matchup = db.fetchone()
    if matchup:
        print_matchup(matchup)
    else:
        print("> No current matchup found")

def view_week_matchups(db):
    week = input("Enter week number (1-17): ")
    if not week.isdigit() or int(week) < 1 or int(week) > 17:
        print("> Invalid week number")
        return
        
    db.execute('''
        SELECT 
            h.team_name as home_team,
            a.team_name as away_team,
            m.home_team_points,
            m.away_team_points,
            m.week
        FROM matchup m
        JOIN team h ON m.home_team_id = h.team_id
        JOIN team a ON m.away_team_id = a.team_id
        WHERE m.week = ?
        ORDER BY m.home_team_points + m.away_team_points DESC
    ''', (week,))
    
    matchups = db.fetchall()
    if matchups:
        print(f"\n=== Week {week} Matchups ===")
        for matchup in matchups:
            print_matchup(matchup)
    else:
        print(f"> No matchups found for week {week}")

def matchup_menu(db):
    while True:
        print("===================================")
        print("Matchup Menu")
        print("===================================")
        print("1. View Current Matchup")
        print("2. View Week's Matchups")
        print("Q. Back to Main Menu")
        print("===================================")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            view_current_matchup(db)
        elif choice == "2":
            view_week_matchups(db)
        elif choice.upper() == "Q":
            break
        else:
            print("> Invalid choice")

def view_all_players(db):
    while True:
        print("===================================")
        print("Viewing All Teams")
        print("===================================")
        db.execute('''SELECT DISTINCT real_team FROM player''')
        teams = db.fetchall()
        
        # List teams on four lines, with 8 teams per line
        teams_per_line = 8
        for i in range(0, len(teams), teams_per_line):
            print(", ".join(team[0] for team in teams[i:i + teams_per_line]))

        # Allow user to select a real team
        selected_team = input("Enter the real team to view players for (Q to quit): ")
        if selected_team.lower() == 'q':
            break
        if selected_team not in [team[0] for team in teams]:
            print("===================================")
            print("Invalid team. Please try again.")
            continue

        # give the option to see all players or only see available players
        only_available = input("View only available players? (Y/N): ")

        # Return all players for the selected real team
        print("===================================")
        print("Viewing Players for " + selected_team)
        print("===================================")
        query = '''SELECT player_name, position, real_team
                    FROM player
                    WHERE real_team = ?'''
        
        if only_available.lower() == 'y':
            query += ''' AND team_id = 0 OR team_id IS NULL'''

        db.execute(query, (selected_team,))
        results = db.fetchall()
        headers = ["Player Name", "Position", "Real Team"]
        print_table(headers, results)


if __name__ == "__main__":
    db_connection = sqlite3.connect(CONNECTION_STRING)
    db = db_connection.cursor()
    main_menu(db)

    while(True):
        print("Home Menu")
        print("===================================")
        print(f"1. {USER.username}'s Roster")
        print("2. View Player Statistics")
        print("3. View all players")
        print("4. Matchups")  # New option
        print("L. Logout")
        print("===================================")

        choice = input("Enter your choice: ")

        if choice == "L" or choice == "l":
            print(f"=== Thank you for using the CLI Fantasy League, {USER.username}! ===")
            main_menu(db)
        elif choice == "1":
            roster_menu(db)
        elif choice == "2":
            player_statistics(db)
        elif choice == "3":
            view_all_players(db)
        elif choice == "4":
            matchup_menu(db)
        else:
            print("> Invalid choice. Please try again.")