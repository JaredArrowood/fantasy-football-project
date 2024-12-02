SELECT * 
    FROM player_statistics
    WHERE player_id = (SELECT player_id
                        FROM player
                        WHERE player_name = 'C.J. Stroud' AND week = 12)