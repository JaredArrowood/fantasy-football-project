# CLI Fantasy Football (CLIFF)

## Instructions for the test queries

1. From the commandline, run the following command to startup the sqlite shell:

   ```cmd
   sqlite3 fantasy_league.db
   ```

2. To run each SQL query, type the name of the query file in the commandline. For example:

   ```cmd
   .read test_query_1.sql
   ```

3. To exit the sqlite3 shell, type:

   ```cmd
   .exit
   ```

## Instructions to run the CLI

1. Make sure you're in the project directory. If you are in the Code directory, it will create a new database file in the Code directory, which is not what you want.

2. From the commandline, run the following command to startup CLIFF:

   ```cmd
   python Code/cli.py
   ```

3. Follow the instructions on the screen to navigate through the CLI. If you want an account that is already populated with data, use the following credentials:

   - Username: `JJefferson@gmail.com`
   - Password: `password2`
