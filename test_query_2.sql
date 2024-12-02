WITH team_players(player_id, is_starting) AS (
    SELECT DISTINCT player.player_id, is_starting
        FROM team, player, player_statistics
        WHERE player.team_id = team.team_id AND team.email = 'JJefferson@gmail.com' AND player.player_id = player_statistics.player_id
)
SELECT player_name, position, real_team, is_starting
    FROM team_players, player
    WHERE team_players.player_id = player.player_id