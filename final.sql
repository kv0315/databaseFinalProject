-- CREATE TABLE nfl_game_stats (
--     Season INT,
--     Team_Full_Name VARCHAR(50),
--     Team_Abr VARCHAR(3),
--     Week FLOAT,
--     Date DATE,
--     Day CHAR(3),
--     is_Home VARCHAR(1),
--     Opp_Full_Name VARCHAR(50),
--     Opp_Abr VARCHAR(3),
--     Game_Result VARCHAR(1),
--     Home_Points_Scored INT,
--     Opp_Points_Scored INT,
--     went_to_overtime VARCHAR(1),
--     Pass_Completions INT,
--     Pass_Attempts INT,
--     Completion_Percentage FLOAT,
--     Pass_Yards INT,
--     Pass_TD INT,
--     Pass_YPA FLOAT,
--     Adjusted_YPA FLOAT,
--     Passer_Rating FLOAT,
--     Sacks_Taken INT,
--     Sack_Yards INT,
--     Rush_Attempts INT,
--     Rush_Yards INT,
--     Rush_TD INT,
--     Rush_YPA FLOAT,
--     Total_Offensive_Plays INT,
--     Total_Yards INT,
--     Yards_Per_Play FLOAT,
--     Field_Goal_Attempts INT,
--     Field_Goals_Made INT,
--     Extra_Point_Attempts INT,
--     Extra_Points_Made INT,
--     Times_Punted INT,
--     Total_Punt_Yards INT,
--     First_Downs_From_Passing INT,
--     First_Downs_From_Rushing INT,
--     First_Downs_From_Penalty INT,
--     Total_First_Downs INT,
--     Third_Down_Conversions INT,
--     Thirds_Down_Attempts INT,
--     Fourth_Down_Conversions INT,
--     Fourth_Down_Attempts INT,
--     Penalties_Commited INT,
--     Penalty_Yards INT,
--     Fumbles_Lost INT,
--     Interceptions_Thrown INT,
--     Turnovers INT,
--     Time_Of_Posession VARCHAR(15)
-- );

-- \copy nfl_game_stats FROM '/u/eu/il/kvaldez/Database/databaseFinalProject/nfl_data.csv' DELIMITER ',' CSV HEADER;

-------------------------------------------------------------------------------------------------------------
-- Create and insert data into the table team
-- CREATE TABLE team (
--     team_id SERIAL PRIMARY KEY CHECK (team_id < 33),
--     team_name VARCHAR(50) NOT NULL,
--     team_abr VARCHAR(5) NOT NULL
-- );


-- INSERT INTO team (team_name, team_abr) SELECT DISTINCT Team_Full_Name, Team_Abr FROM nfl_game_stats;
-------------------------------------------------------------------------------------------------------------



-------------------------------------------------------------------------------------------------------------
-- Create and insert data into the game_details table
CREATE TABLE game_details (
    game_id SERIAL PRIMARY KEY,
    season INT,
    week FLOAT,
    date DATE,
    is_Home VARCHAR(1),
    Team_Full_Name INT REFERENCES team(team_name),
    Opp_Full_Name INT REFERENCES team(team_name),
    Game_Result VARCHAR(1),
    went_to_overtime VARCHAR(1),
    Time_Of_Posession VARCHAR(15),
    CONSTRAINT chk_different_teams CHECK (team_id <> opp_team_id)
);

-- INSERT INTO game_details (season, week, date, is_Home, team_id, opp_team_id, Game_Result, went_to_overtime, Time_Of_Posession) 
-- SELECT season, week, date, is_Home, t.team_id AS team_id, opp.team_id AS opp_id,Game_Result, went_to_overtime, Time_Of_Posession FROM nfl_game_stats g
-- JOIN team t ON g.Team_Full_Name = t.team_name
-- JOIN team opp ON g.Opp_Full_Name = opp.team_name
-- ORDER BY team_id, season, week;

-------------------------------------------------------------------------------------------------------------
-- Create the statline table
-- CREATE TABLE statline (
--     stat_id SERIAL PRIMARY KEY,
--     game_id INT REFERENCES game_details(game_id),
--     team_id INT REFERENCES team(team_id),
--     points_scored INT,
--     points_allowed INT,
--     Total_Offensive_Plays INT,
--     Total_Yards INT,
--     Yards_Per_Play FLOAT,
--     Penalties_Commited INT,
--     Penalty_Yards INT
-- );

-- INSERT INTO statline (
--     game_id, team_id, is_Home, points_scored, points_allowed,
--     Total_Offensive_Plays, Total_Yards, Yards_Per_Play,
--     Penalties_Commited, Penalty_Yards
-- )
-- SELECT 
--     d.game_id,
--     d.team_id,
--     d.opp_team_id
--     d.is_Home,
--     g.Home_Points_Scored,
--     g.Opp_Points_Scored,
--     g.Total_Offensive_Plays,
--     g.Total_Yards,
--     g.Yards_Per_Play,
--     g.Penalties_Commited,
--     g.Penalty_Yards
-- FROM nfl_game_stats g
-- JOIN game_details d ON d.team_id = d.team_id AND d;

-- SELECT t.team_name, points_scored, points_allowed FROM statline s
-- JOIN team t ON t.team_id = s.team_id
-- WHERE t.team_name = 'Denver Broncos' AND points_allowed > 50;
-- -- Create the rushing_stats table
-- CREATE TABLE rushing_stats (
--     stat_id INT REFERENCES statline(stat_id),
--     Rush_Attempts INT,
--     Rush_Yards INT,
--     Rush_TD INT,
--     Rush_YPA FLOAT
-- );

-- -- Create the passing_stats table
-- CREATE TABLE passing_stats (
--     stat_id INT REFERENCES statline(stat_id),
--     Pass_Attempts INT,
--     Pass_Completions INT,
--     Completion_Percentage FLOAT,
--     Pass_Yards INT,
--     Pass_TD INT,
--     Pass_YPA FLOAT,
--     Adjusted_YPA FLOAT,
--     Passer_Rating FLOAT,
--     Sacks_Taken INT,
--     Sack_Yards INT
-- );

-- -- Create the turnover_stats table
-- CREATE TABLE turnover_stats (
--     stat_id INT REFERENCES statline(stat_id),
--     Fumbles_Lost INT,
--     Interceptions_Thrown INT,
--     turnovers INT
-- );

-- -- Create the first_down_stats table
-- CREATE TABLE first_down_stats (
--     stat_id INT REFERENCES statline(stat_id),
--     First_Downs_From_Passing INT,
--     First_Downs_From_Rushing INT,
--     First_Downs_From_Penalty INT,
--     Total_First_Downs INT
-- );

-- -- Create the conversion_stats table
-- CREATE TABLE conversion_stats (
--     stat_id INT REFERENCES statline(stat_id),
--     Third_Down_Conversions INT,
--     Thirds_Down_Attempts INT,
--     Fourth_Down_Conversions INT,
--     Fourth_Down_Attempts INT
-- );

-- -- Create the kicking_stats table
-- CREATE TABLE kicking_stats (
--     stat_id INT REFERENCES statline(stat_id),
--     Field_Goal_Attempts INT,
--     Field_Goals_Made INT,
--     Extra_Point_Attempts INT,
--     Extra_Points_Made INT,
--     Times_Punted INT,
--     Total_Punt_Yards INT
-- );
