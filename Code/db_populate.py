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


# def populate_team_table(db):
#     db.execute('''

#                '''))

if(__name__ == "__main__"):
    populate_user_table(db)
    conn.commit()
    conn.close()
