SELECT username, team_name
    FROM user, team
    WHERE user.email = team.email AND user.email = 'JJefferson@gmail.com'