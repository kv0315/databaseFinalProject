Kaden Valdez
Aedon Kettles
Component 1: 

Component 1: Dataset(s)
Large Dataset: 
- 7806 Rows
- 50 Columns

Component 2: Application
Data Science and Analysis
-- Extract insights from the data that are not trivially obvious from an inspection of the data
- Able to quickly scan over 14 years of data within seconds rather than have to search on each years different webpage for each time to look at data. 
- Main Data is able to be put into a multi table schema for easier accessablity to different types of data. 
- MAYBE US sciKIT-learn for visuals...


Component 3: Outputs (***NEED 4***)
- Your choice (Data Scraping and Cleaning Using Python):
Used 'https://www.pro-football-reference.com/teams/' + {team} + '/' + {season} + '/gamelog/' for every team from 2010 to 2024 to get every game for each team into a dataframe where we would remove incomplete rows, and the season totals row. We would then clean the column names of the data 
for better read ability because the names are not descriptive. For example the column "Unnamed: 5" correlated to whether that specific game was played at home or away. We also altered the values of the columns "Home", "Result", and "OT" to be binary, so if a team was at Home the corresponding value would be a 1, and away would be a 0. For result a value of 1 would be a win, and a loss would be a 0, finally for the OT (overtime) column a value of 1 says the game went to overtime, and a value 0 says it did not go into overtime. We would also add a column that would add both teams full name rather than just both of their 3 letter abreviations. We would also update all team names and abreviations to the current team name and current team abreviation. For example the "Oakland Raiders" "OAK" with is now "Los Vegas Raiders" "LVR". 

- Database Schema Design: 
CREATE TABLE team (
    team_id SERIAL PRIMARY KEY CHECK (team_id < 33),
    team_name VARCHAR(50) NOT NULL,
    team_abr VARCHAR(5) NOT NULL
);

-- ONLY 32 teams in the NFL, so team_id should never be above 32

CREATE TABLE Game (
    game_id SERIAL PRIMARY KEY,
    season INT NOT NULL,
    week INT NOT NULL,
    date DATE NOT NULL,
    day VARCHAR(10) CHECK (day IN ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')),
    home_team_id INT NOT NULL REFERENCES team(team_id),
    away_team_id INT NOT NULL REFERENCES team(team_id),
    game_result VARCHAR(1) CHECK (game_result in ('W', 'T', 'L')),
    overtime BOOLEAN, 
    time_of_possession VARCHAR(20),
    CONSTRAINT chk_different_teams CHECK (home_team_id <> away_team_id)
);

-- Constraint to make sure the home_team_id and the away_team_id are different

CREATE TABLE TeamStats (
    stats_id SERIAL PRIMARY KEY,
    game_id INT NOT NULL REFERENCES Game(game_id) ON DELETE CASCADE,
    team_id INT NOT NULL REFERENCES Team(team_id),
    is_home BOOLEAN NOT NULL,
    points_scored INT,
    pass_completions INT,
    pass_attempts INT,
    completion_percentage FLOAT,
    pass_yards INT,
    pass_TD INT,
    pass_YPA FLOAT,
    adjusted_YPA FLOAT,
    passer_rating FLOAT,
    sacks_taken INT,
    sack_yards INT,
    rush_attempts INT,
    rush_yards INT,
    rush_TD INT,
    rush_YPA FLOAT,
    total_offensive_plays INT,
    total_yards INT,
    yards_per_play FLOAT,
    field_goal_attempts INT,
    field_goals_made INT,
    extra_point_attempts INT,
    extra_points_made INT,
    times_punted INT,
    total_punt_yards INT,
    first_downs_pass INT,
    first_downs_rush INT,
    first_downs_penalty INT,
    total_first_downs INT,
    third_down_conversions INT,
    third_down_attempts INT,
    fourth_down_conversions INT,
    fourth_down_attempts INT,
    penalties_committed INT,
    penalty_yards INT,
    fumbles_lost INT,
    interceptions_thrown INT,
    turnovers INT,
    CONSTRAINT unique_game_team UNIQUE (game_id, team_id)
);                

-- Contraints to avoid having multiple games for the same team_id and game_id
-- ON DELETE CASCADE deletes all the stats if a game_id if deleted 


