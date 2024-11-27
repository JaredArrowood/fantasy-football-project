import sqlite3 as sql

conn = sql.connect('fantasy_league.db')
db = conn.cursor()

def populate_user_table(db):
    db.execute('''
    INSERT INTO user (email, username, password)
    VALUES ('jaredarrowood@gmail.com', 'jared', 'password')
    ''')
    db.execute('''
    INSERT INTO user (email, username, password)
    VALUES ('hoowahwin@gmail.com', 'hoowah', 'password')
    ''')

    #attempt to add a duplicate email
    # db.execute('''
    # INSERT INTO user (email, username, password)
    # VALUES ('hoowahwin@gmail.com', 'hoowah1', 'password')
    # ''')


def populate_team_table(db):
    db.execute('''
    INSERT INTO team (team_id, team_name, email)
               VALUES(1, 'team1', 'jaredarrowood@gmail.com')
    ''')
    db.execute('''
               INSERT into team (team_id, team_name, email)
                VALUES(2, 'team2', 'hoowahwin@gmail.com')
               ''')
    
def populate_player_table(db):
    db.execute('''
    INSERT INTO player (player_id, player_name, position, real_team, injury_status, team_id)
    VALUES(1, 'Tom Brady', 'QB', 'TB', 'Healthy', 0)
    ''')
    db.execute('''
    INSERT INTO player (player_id, player_name, position, real_team, injury_status, team_id)
    VALUES(2, 'Dak Prescott', 'QB', 'DAL', 'Healthy', 1)
    ''')
    db.execute('''
    INSERT INTO player (player_id, player_name, position, real_team, injury_status, team_id)
    VALUES(3, 'Patrick Mahomes', 'QB', 'KC', 'Healthy', 2)
    ''')
    db.execute('''
    INSERT INTO player (player_id, player_name, position, real_team, injury_status, team_id)
    VALUES(4, 'Russell Wilson', 'QB', 'SEA', 'Healthy', 2)
    ''')
    db.execute('''
    INSERT INTO player (player_id, player_name, position, real_team, injury_status, team_id)
               VALUES(5, 'Chris Boswell', 'K', 'PIT', 'Healthy', 1)
    ''')

def populate_matchup_table(db):
    db.execute('''
    INSERT INTO matchup (week, home_team_id, away_team_id, away_team_points, home_team_points)
    VALUES(1, 1, 2, 100, 90)
               ''')

def populate_kicker_statistics(db):
    db.execute('''
    INSERT INTO kicker_statistics (player_id, week, field_goals_made, field_goals_attempted, extra_points_made, extra_points_attempted, total_points, is_starting)
    VALUES(5, 1, 2, 2, 5, 5, 11, True)
    ''')

def populate_player_statistics(db):
    db.execute('''
               INSERT into player_statistics(player_id, week, passing_yards, rushing_yards, passing_td, rushing_td, receptions, fumbles, interceptions, total_points, is_starting)
               VALUES(1, 1, 300, 0, 3, 0, 0, 0, 0, 0, True)
               ''')
    db.execute('''
                INSERT into player_statistics(player_id, week, passing_yards, rushing_yards, passing_td, rushing_td, receptions, fumbles, interceptions, total_points, is_starting)
                VALUES(2, 1, 400, 0, 4, 0, 0, 0, 0, 0, True)
                ''')
    db.execute('''
                INSERT into player_statistics(player_id, week, passing_yards, rushing_yards, passing_td, rushing_td, receptions, fumbles, interceptions, total_points, is_starting)
                VALUES(3, 1, 500, 0, 5, 0, 0, 0, 0, 0, True)
                ''')
    db.execute('''
                INSERT into player_statistics(player_id, week, passing_yards, rushing_yards, passing_td, rushing_td, receptions, fumbles, interceptions, total_points, is_starting)
                VALUES(4, 1, 600, 0, 6, 0, 0, 0, 0, 0, True)
                ''')

if(__name__ == "__main__"):
    populate_user_table(db)
    populate_team_table(db)
    populate_player_table(db)
    populate_matchup_table(db)
    populate_kicker_statistics(db)  
    populate_player_statistics(db)

    conn.commit()
    conn.close()
