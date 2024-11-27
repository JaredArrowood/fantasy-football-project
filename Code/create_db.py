import sqlite3

# won't be needed once the database is created
conn = sqlite3.connect('fantasy_league.db')

db = conn.cursor()

# drop tables if they exist
db.execute('DROP TABLE IF EXISTS user')
db.execute('DROP TABLE IF EXISTS team')
db.execute('DROP TABLE IF EXISTS matchup')
db.execute('DROP TABLE IF EXISTS player')
db.execute('DROP TABLE IF EXISTS defense_st')
db.execute('DROP TABLE IF EXISTS player_statistics')
db.execute('DROP TABLE IF EXISTS kicker_statistics')
db.execute('DROP TABLE IF EXISTS defense_st_statistics')

# user table
db.execute('''
CREATE TABLE user (
    email TEXT PRIMARY KEY NOT NULL unique,
    username CHAR(100) NOT NULL,
    password CHAR(100) NOT NULL
)
''')

# team table
db.execute('''
CREATE TABLE team (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name CHAR(100) NOT NULL,
    email INTEGER NOT NULL,
    FOREIGN KEY (email) REFERENCES user(email)
)
''')

conn.commit()

# matchup table
db.execute('''
CREATE TABLE matchup (
    week INTEGER NOT NULL,
    home_team_id INTEGER NOT NULL,
    away_team_id INTEGER NOT NULL,
    away_team_points INTEGER NOT NULL,
    home_team_points INTEGER NOT NULL,
    FOREIGN KEY (home_team_id) REFERENCES team(team_id),
    FOREIGN KEY (away_team_id) REFERENCES team(team_id)
    PRIMARY KEY (week, home_team_id, away_team_id),
    CHECK (home_team_id != away_team_id)
)
''')

# player table
db.execute('''
CREATE TABLE player (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name CHAR(100) NOT NULL,
    position CHAR(100) NOT NULL,
    real_team CHAR(100) NOT NULL,
    injury_status CHAR(100) NOT NULL,
    team_id INTEGER,
    FOREIGN KEY (team_id) REFERENCES team(team_id)
)
''')

# defense_st table
db.execute('''
CREATE TABLE defense_st (
    defense_st_id INTEGER PRIMARY KEY AUTOINCREMENT,
    real_team CHAR(100) NOT NULL,
    team_id INTEGER,
    FOREIGN KEY (team_id) REFERENCES team(team_id)
)
''')

# player_statistics table

db.execute('''
CREATE TABLE player_statistics (
    player_id INTEGER NOT NULL,
    week INTEGER NOT NULL,
    passing_yards INTEGER NOT NULL,
    rushing_yards INTEGER NOT NULL,
    passing_td INTEGER NOT NULL,
    rushing_td INTEGER NOT NULL,
    receptions INTEGER NOT NULL,
    fumbles INTEGER NOT NULL,
    interceptions INTEGER NOT NULL,
    total_points INTEGER NOT NULL,
    is_starting BOOLEAN NOT NULL,
    FOREIGN KEY (player_id) REFERENCES player(player_id),
    PRIMARY KEY (player_id, week)
)
''')

# kicker_statistics table
db.execute('''
CREATE TABLE kicker_statistics (
    player_id INTEGER NOT NULL,
    week INTEGER NOT NULL,
    field_goals_made INTEGER NOT NULL,
    field_goals_attempted INTEGER NOT NULL,
    extra_points_made INTEGER NOT NULL,
    extra_points_attempted INTEGER NOT NULL,
    total_points INTEGER NOT NULL,
    is_starting BOOLEAN NOT NULL,
    FOREIGN KEY (player_id) REFERENCES player(player_id),
    PRIMARY KEY (player_id, week)
)
''')

# defense_st_statistics table
db.execute('''
CREATE TABLE defense_st_statistics (
    defense_st_id INTEGER NOT NULL,
    week INTEGER NOT NULL,
    interceptions_recovered INTEGER NOT NULL,
    def_touchdowns INTEGER NOT NULL,
    fumbles_recovered INTEGER NOT NULL,
    yards_allowed INTEGER NOT NULL,
    points_allowed INTEGER NOT NULL,
    total_points INTEGER NOT NULL,
    is_starting BOOLEAN NOT NULL,
    FOREIGN KEY (defense_st_id) REFERENCES defense_st(defense_st_id),
    PRIMARY KEY (defense_st_id, week)
)
''')

conn.commit()
