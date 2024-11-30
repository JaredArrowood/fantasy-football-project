import sqlite3
from espn_api.football import League
from espn_api.football import Team

# Database connection
conn = sqlite3.connect('fantasy_league.db')
cursor = conn.cursor()

# ESPN API League setup
league = League(
    league_id=2144731,  # Your league ID
    year=2024,          # Fantasy season year
    espn_s2="AEB6N9U4WIkrBzbD%2FiNeUI%2FKJP1Y2sN4pwxcgZKHT8z%2BHnIVaKnTe5mBWqJWC9ySkNRomw%2BYZIF8rRfFXl4ZSS15VBLeczrOT1SAWyih7Mw4VulziUoq3pUw8ozP9zAkvKcbzMCt2eMr349g7rKjEFxgRFBNZhToy3ferv33g2p7YpbpxIVDPY7Ifte6RVZVqVn3h7Pvlamvo%2BHX97sot%2F0Cmp9sDBIGKoWyT9brp1LPw%2F3YoYxXD6HTtXo7QkMatSSdYZqJCGqxtNE2GavF6Zn9JgKQog05fd8Gz%2BrqAdu%2Fmw%3D%3D",  # Replace with your espn_s2 cookie
    swid="{8B95A023-6BA3-45E0-B398-1063ED5EB638}"       # Replace with your swid cookie
)

# Team name mapping function
def modify_team_name(original_name, team_number):
    """
    Modify team names for database storage.
    Example: 'Team Awesome' -> 'Fantasy Awesome'
    """

    if team_number == 1:
        return "JJettas"
    elif team_number == 2:
        return "Jamar Chase is my Dad"
    elif team_number == 3:
        return "Joe Shiesty"
    elif team_number == 4:
        return "Lebron James is my Dad"
    elif team_number == 5:
        return "Maliks nabers"
    elif team_number == 6:
        return "tyrannosaurus mathieu"
    elif team_number == 7:
        return "scary terry"
    elif team_number == 8:
        return "baskemball"
    elif team_number == 9:
        return "I love puka nacua"
    elif team_number == 10:
        return "please give me saquon"
    elif team_number == 11:
        return "AdamBenHaBallerz"
    elif team_number == 12:
        return "Blake Bortles"

    return f"Fantasy {original_name.split()[-1]}"
def modify_username(original_name, team_number):
    """
    Modify team names for database storage.
    Example: 'Team Awesome' -> 'Fantasy Awesome'
    """

    if team_number == 1:
        return "JJefferson"
    elif team_number == 2:
        return "JChase"
    elif team_number == 3:
        return "JBurrow"
    elif team_number == 4:
        return "Lebron"
    elif team_number == 5:
        return "MNabers"
    elif team_number == 6:
        return "TMathieu"
    elif team_number == 7:
        return "scary"
    elif team_number == 8:
        return "bball"
    elif team_number == 9:
        return "pnacua"
    elif team_number == 10:
        return "sbarkley"
    elif team_number == 11:
        return "AdamBenUsername"
    elif team_number == 12:
        return "BBortles"

    return f"Fantasy {original_name.split()[-1]}"
# Populate teams in the database
team_number = 1
for team in league.teams[:10]:  # Only populate the first 10 teams
    modified_name = modify_team_name(team.team_name, team_number)
    modified_username = modify_username(team.team_name, team_number)
    team_number += 1
    try:
        cursor.execute("""
            INSERT INTO team (team_id, team_name, email)
            VALUES (?, ?, ?)
            ON CONFLICT (team_id) DO NOTHING
        """, (team.team_id, modified_name, modified_username + "@gmail.com"))  # Fixed concatenation
        cursor.execute("""
            INSERT INTO user (email, username, password)
            VALUES (?, ?, ?)
            ON CONFLICT (email) DO NOTHING
        """, (modified_username + "@gmail.com", modified_username, "password" + str(team_number)))
    except sqlite3.Error as e:
        print(f"Error inserting team {team.team_id}: {e}")

# Populate players in the database
for team in league.teams:
    for player in team.roster:
        try:
            if player.position == "D/ST":
                # Defense/ST player
                cursor.execute("""
                    INSERT INTO defense_st (defense_st_id, real_team, team_id)
                    VALUES (?, ?, ?)
                    ON CONFLICT (defense_st_id) DO NOTHING
                """, (player.playerId, player.proTeam, team.team_id))
            else:
                team_id = team.team_id 
                cursor.execute("""
                    INSERT INTO player (player_id, player_name, position, real_team, injury_status, team_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT (player_id) DO NOTHING
                """, (
                    player.playerId,
                    player.name,
                    player.position,
                    player.proTeam,  # Real NFL team abbreviation
                    player.injuryStatus,
                    team_id
                ))
        except sqlite3.Error as e:
            print(f"Error inserting player {player.player_id}: {e}")
positions = ["QB", "RB", "WR", "TE", "K", "D/ST"]
for position in positions:
    free_agents = league.free_agents(position=position)  # Get free agents for the position
    top_free_agents = free_agents[:10]  # Limit to the top 10

    for player in top_free_agents:
        try:
            if player.position == "D/ST":
                # Defense/ST player
                cursor.execute("""
                    INSERT INTO defense_st (defense_st_id, real_team, team_id)
                    VALUES (?, ?, ?)
                    ON CONFLICT (defense_st_id) DO NOTHING
                """, (player.playerId, player.proTeam, 0))
            else:
                team_id = team.team_id 
                cursor.execute("""
                    INSERT INTO player (player_id, player_name, position, real_team, injury_status, team_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT (player_id) DO NOTHING
                """, (
                    player.playerId,
                    player.name,
                    player.position,
                    player.proTeam,  # Real NFL team abbreviation
                    player.injuryStatus,
                    0
                ))
        except sqlite3.Error as e:
            print(f"Error inserting player {player.player_id}: {e}")
def populate_matchups(week):
    """
    Populate matchups for the specified week.
    """
    matchup_id = 1
    seen_matchups = set()  # Track processed matchups to avoid duplicates

    for team in league.teams:
        # Ensure the week is within the schedule's range
        if week - 1 >= len(team.schedule):
            print(f"Week {week} is out of range for team {team.team_name}")
            continue

        # Get the opponent for the current week
        opponent = team.schedule[week - 1]  # Use list indexing

        # Skip if no opponent or opponent is a placeholder
        if not opponent or not hasattr(opponent, "team_id"):
            print(f"No valid opponent for team {team.team_name} in Week {week}")
            continue

        # Create a unique matchup identifier to avoid duplicates
        matchup_key = tuple(sorted((team.team_id, opponent.team_id)))
        if matchup_key in seen_matchups:
            continue
        seen_matchups.add(matchup_key)

        try:
            # Insert the matchup into the database
            cursor.execute("""
                INSERT INTO matchup (home_team_id, away_team_id, home_team_points, away_team_points, week)
                VALUES (?, ?, ?, ?, ?)
            """, (
                team.team_id,  # Home team
                opponent.team_id,  # Away team
                team.scores[week - 1] if week - 1 < len(team.scores) else 0,  # Home team points
                opponent.scores[week - 1] if week - 1 < len(opponent.scores) else 0,  # Away team points
                week
            ))
            print(f"Inserted matchup: {team.team_id} vs {opponent.team_id} for Week {week}")
        except Exception as e:
            print(f"Error inserting matchup {week}: {e}")


# Fetch weekly statistics
def populate_weekly_stats(week):
    """
    Populate player and team statistics for the given week.
    """
    for team in league.teams:
        for player in team.roster:
            # Check if stats are available for the given week
            if week in player.stats:
                stats = player.stats.get(week, {})  # Fetch stats for the week
            else:
                stats = {}  # Default to empty stats if unavailable
         
            try:
                if player.position == "K":  # Kicker stats
                    team_stats = player.stats.get(week, {})
                    field_goals_made = float(team_stats.get('breakdown', {}).get('madeFieldGoalsFromUnder40', 0) +
                                            team_stats.get('breakdown', {}).get('madeFieldGoalsFrom40To49', 0) +
                                            team_stats.get('breakdown', {}).get('madeFieldGoalsFrom60Plus', 0))
                    field_goals_attempted = float(field_goals_made + team_stats.get('breakdown', {}).get('missedFieldGoals', 0))
                    extra_points_made = float(team_stats.get('breakdown', {}).get('madeExtraPoints', 0))
                    total_points_kicker = float(team_stats.get('points', 0))
                    cursor.execute("""
                        INSERT INTO kicker_statistics (
                            player_id, week, field_goals_made, field_goals_attempted, extra_points_made,
                            extra_points_attempted, total_points, is_starting
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        player.playerId,
                        week,
                        field_goals_made,
                        field_goals_attempted,
                        extra_points_made,
                        extra_points_made,  # Assume no missed extra points
                        total_points_kicker,
                        player.lineupSlot != "BE"  # Check if player is starting
                    ))

                elif player.position in ["QB", "RB", "WR", "TE"]:  # Offensive player stats
                    cursor.execute("""
                        INSERT INTO player_statistics (
                            player_id, week, passing_yards, rushing_yards, receiving_yards, passing_td, rushing_td, recieving_td,
                            receptions, fumbles, interceptions, total_points, is_starting
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        player.playerId,
                        week,
                        float(stats.get('breakdown', {}).get('passingYards', 0)),
                        float(stats.get('breakdown', {}).get('rushingYards', 0)),
                        float(stats.get('breakdown', {}).get('receivingYards', 0)),
                        float(stats.get('breakdown', {}).get('passingTouchdowns', 0)),
                        float(stats.get('breakdown', {}).get('rushingTouchdowns', 0)),
                        float(stats.get('breakdown', {}).get('receivingTouchdowns', 0)),
                        float(stats.get('breakdown', {}).get('receivingReceptions', 0)),
                        float(stats.get('breakdown', {}).get('fumbles', 0)),
                        float(stats.get('breakdown', {}).get('interceptions', 0)),
                        float(stats.get('points', 0)),  # Total points for the week
                        player.lineupSlot != "BE"  
                    ))
                elif player.position == "D/ST":  # Defensive stats
                    team_stats = player.stats.get(week, {})
                    
                    yards_allowed = float(team_stats.get('breakdown', {}).get('defensiveYardsAllowed', 0))
                    points_allowed = float(team_stats.get('breakdown', {}).get('defensivePointsAllowed', 0))
    
                    total_points_defense = float(team_stats.get('points', 0))
    
                    cursor.execute("""
                        INSERT INTO defense_st_statistics (
                            defense_st_id, week, interceptions, def_touchdowns, fumbles_recovered, sacks,
                            yards_allowed, points_allowed, total_points, is_starting
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        player.playerId,
                        week,
                        float(team_stats.get('breakdown', {}).get('defensiveInterceptions', 0)),
                        float(team_stats.get('breakdown', {}).get('defensiveTouchdowns', 0) +
                              team_stats.get('breakdown', {}).get('fumbleReturnTouchdowns', 0) +
                              team_stats.get('breakdown', {}).get('puntReturnTouchdowns', 0) +
                              team_stats.get('breakdown', {}).get('kickoffReturnTouchdowns', 0)),
                        float(team_stats.get('breakdown', {}).get('defensiveFumbles', 0)),
                        float(team_stats.get('breakdown', {}).get('defensiveSacks', 0)),
                        yards_allowed,
                        points_allowed,
                        total_points_defense,
                        player.lineupSlot != "BE"
                    ))
            except Exception as e:
                print(f"Error inserting stats for player {player.name}: {e}")

def populate_weekly_fa_stats(week):
    positions = ["QB", "RB", "WR", "TE", "K", "D/ST"]
    for position in positions:
        free_agents = league.free_agents(position=position, size=10)  # Get top 10 free agents for the position

        for player in free_agents:
            if week in player.stats:
                stats = player.stats.get(week, {})  # Fetch stats for the week
            else:
                stats = {}  # Default to empty stats if unavailable
           
            try:
                if player.position == "K":  # Kicker stats
                
                    team_stats = player.stats.get(week, {})
                    field_goals_made = float(team_stats.get('breakdown', {}).get('madeFieldGoals', 0))
                    field_goals_attempted = float(team_stats.get('breakdown', {}).get('attemptedFieldGoals', 0))
                    extra_points_made = float(team_stats.get('breakdown', {}).get('madeExtraPoints', 0))
                    extra_points_attempted = float(team_stats.get('breakdown', {}).get('attemptedExtraPoints', 0))
                    total_points_kicker = float(team_stats.get('points', 0))
                    cursor.execute("""
                        INSERT INTO kicker_statistics (
                            player_id, week, field_goals_made, field_goals_attempted, extra_points_made,
                            extra_points_attempted, total_points, is_starting
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        player.playerId,
                        week,
                        field_goals_made,
                        field_goals_attempted,
                        extra_points_made,
                        extra_points_attempted,  # Assume no missed extra points
                        total_points_kicker,
                        player.lineupSlot != "BENCH"  # Check if player is starting
                    ))

                elif player.position in ["QB", "RB", "WR", "TE"]:  # Offensive player stats
                    cursor.execute("""
                        INSERT INTO player_statistics (
                            player_id, week, passing_yards, rushing_yards, receiving_yards, passing_td, rushing_td, recieving_td,
                            receptions, fumbles, interceptions, total_points, is_starting
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        player.playerId,
                        week,
                        float(stats.get('breakdown', {}).get('passingYards', 0)),
                        float(stats.get('breakdown', {}).get('rushingYards', 0)),
                        float(stats.get('breakdown', {}).get('receivingYards', 0)),
                        float(stats.get('breakdown', {}).get('passingTouchdowns', 0)),
                        float(stats.get('breakdown', {}).get('rushingTouchdowns', 0)),
                        float(stats.get('breakdown', {}).get('receivingTouchdowns', 0)),
                        float(stats.get('breakdown', {}).get('receivingReceptions', 0)),
                        float(stats.get('breakdown', {}).get('fumbles', 0)),
                        float(stats.get('breakdown', {}).get('interceptions', 0)),
                        float(stats.get('points', 0)),  # Total points for the week
                        player.injured  # Assuming injured status determines is_starting
                    ))
                elif player.position == "D/ST":  # Defensive stats
                    team_stats = player.stats.get(week, {})
                    
                    yards_allowed = float(team_stats.get('breakdown', {}).get('defensiveYardsAllowed', 0))
                    points_allowed = float(team_stats.get('breakdown', {}).get('defensivePointsAllowed', 0))
    
                    total_points_defense = float(team_stats.get('points', 0))
    
                    cursor.execute("""
                        INSERT INTO defense_st_statistics (
                            defense_st_id, week, interceptions, def_touchdowns, fumbles_recovered, sacks,
                            yards_allowed, points_allowed, total_points, is_starting
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        player.playerId,
                        week,
                        float(team_stats.get('breakdown', {}).get('defensiveInterceptions', 0)),
                        float(team_stats.get('breakdown', {}).get('defensiveTouchdowns', 0) +
                              team_stats.get('breakdown', {}).get('fumbleReturnTouchdowns', 0) +
                              team_stats.get('breakdown', {}).get('puntReturnTouchdowns', 0) +
                              team_stats.get('breakdown', {}).get('kickoffReturnTouchdowns', 0)),
                        float(team_stats.get('breakdown', {}).get('defensiveFumbles', 0)),
                        float(team_stats.get('breakdown', {}).get('defensiveSacks', 0)),
                        yards_allowed,
                        points_allowed,
                        total_points_defense,
                        player.lineupSlot != "BENCH"  # Check if player is starting
                    ))
            except Exception as e:
                print(f"Error inserting stats for player {player.name}: {e}")

# Populate data for all weeks in the season

for week in range(1, league.settings.reg_season_count + 1):
    print(f"Populating data for Week {week}...")
    populate_matchups(week)
    populate_weekly_stats(week)
    populate_weekly_fa_stats(week)

# Commit changes to database
conn.commit()
conn.close()
