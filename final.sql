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
-- CREATE TABLE game (
--     game_id SERIAL PRIMARY KEY,
--     season INT,
--     week FLOAT,
--     date DATE,
--     day VARCHAR(5),
--     is_Home VARCHAR(1),
--     Game_Result VARCHAR(1),
--     Team_Full_Name VARCHAR(50),
--     Opp_Full_Name VARCHAR(50),
--     went_to_overtime VARCHAR(1),
--     Time_Of_Posession VARCHAR(15),
--     CONSTRAINT chk_different_teams CHECK (Team_Full_Name <> Opp_Full_Name)
-- );

-- INSERT INTO game (season, week, date, is_Home, Team_Full_Name, Opp_Full_Name, Game_Result, went_to_overtime, Time_Of_Posession)
-- SELECT season, week, date, is_Home, Team_Full_Name, Opp_Full_Name, Game_Result, went_to_overtime, Time_Of_Posession FROM nfl_game_stats g;
-------------------------------------------------------------------------------------------------------------
-- Create the statline table
-- CREATE TABLE statline (
--     stat_id SERIAL PRIMARY KEY,
--     game_id INT REFERENCES game(game_id),
--     Team_Full_Name VARCHAR(50),
--     points_scored INT,
--     points_allowed INT,
--     Total_Offensive_Plays INT,
--     Total_Yards INT,
--     Yards_Per_Play FLOAT,
--     Penalties_Commited INT,
--     Penalty_Yards INT
-- );

-- INSERT INTO statline (game_id, Team_Full_Name, points_scored, points_allowed, Total_Offensive_Plays, Total_Yards, Yards_Per_Play, Penalties_Commited, Penalty_Yards )
-- SELECT d.game_id, g.Team_Full_Name, g.Home_Points_Scored, g.Opp_Points_Scored, g.Total_Offensive_Plays, g.Total_Yards, g.Yards_Per_Play, g.Penalties_Commited, g.Penalty_Yards
-- FROM nfl_game_stats g
-- JOIN game d ON g.Team_Full_Name = d.Team_Full_Name AND g.Opp_Full_Name = d.Opp_Full_Name AND g.week = d.week AND g.season = d.season
-- ORDER BY d.game_id;

-- Create the rushing_stats table
-- CREATE TABLE rushing_stats (
--     stat_id INT REFERENCES statline(stat_id),
--     Rush_Attempts INT,
--     Rush_Yards INT,
--     Rush_TD INT,
--     Rush_YPA FLOAT
-- );

-- INSERT INTO rushing_stats(stat_id, Rush_Attempts, Rush_Yards, Rush_TD, Rush_YPA)
-- SELECT s.stat_id, g.Rush_Attempts, g.Rush_Yards, g.Rush_TD, g.Rush_YPA
-- FROM nfl_game_stats g
-- JOIN statline s ON s.Team_Full_Name = g.Team_Full_Name AND s.points_scored = g.Home_Points_Scored AND s.points_allowed = g.Opp_Points_Scored AND s.Total_Yards = g.Total_Yards AND s.Yards_Per_Play = g.Yards_Per_Play;


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

-- INSERT INTO passing_stats (stat_id, Pass_Attempts, Pass_Completions, Completion_Percentage, Pass_Yards, Pass_TD, Pass_YPA, Adjusted_YPA, Passer_Rating, Sacks_Taken, Sack_Yards)
-- SELECT s.stat_id, g.Pass_Attempts, g.Pass_Completions, g.Completion_Percentage, g.Pass_Yards, g.Pass_TD, g.Pass_YPA, g.Adjusted_YPA, g.Passer_Rating, g.Sacks_Taken, g.Sack_Yards
-- FROM nfl_game_stats g
-- JOIN statline s ON s.Team_Full_Name = g.Team_Full_Name AND s.points_scored = g.Home_Points_Scored AND s.points_allowed = g.Opp_Points_Scored AND s.Total_Yards = g.Total_Yards AND s.Yards_Per_Play = g.Yards_Per_Play
-- ORDER BY stat_id;

-- Create the turnover_stats table
-- CREATE TABLE turnover_stats (
--     stat_id INT REFERENCES statline(stat_id),
--     Fumbles_Lost INT,
--     Interceptions_Thrown INT,
--     turnovers INT
-- );

-- INSERT INTO turnover_stats (stat_id, Fumbles_Lost, Interceptions_Thrown, Turnovers)
-- SELECT s.stat_id, g.Fumbles_Lost, g.Interceptions_Thrown, g.Turnovers
-- FROM nfl_game_stats g
-- JOIN statline s ON s.Team_Full_Name = g.Team_Full_Name AND s.points_scored = g.Home_Points_Scored AND s.points_allowed = g.Opp_Points_Scored AND s.Total_Yards = g.Total_Yards AND s.Yards_Per_Play = g.Yards_Per_Play;

-- -- Create the first_down_stats table
-- CREATE TABLE first_down_stats (
--     stat_id INT REFERENCES statline(stat_id),
--     First_Downs_From_Passing INT,
--     First_Downs_From_Rushing INT,
--     First_Downs_From_Penalty INT,
--     Total_First_Downs INT
-- );

-- INSERT INTO first_down_stats(stat_id, First_Downs_From_Passing, First_Downs_From_Rushing, First_Downs_From_Penalty, Total_First_Downs)
-- SELECT s.stat_id, g.First_Downs_From_Passing, g.First_Downs_From_Rushing, g.First_Downs_From_Penalty, g.Total_First_Downs
-- FROM nfl_game_stats g
-- JOIN statline s ON s.Team_Full_Name = g.Team_Full_Name AND s.points_scored = g.Home_Points_Scored AND s.points_allowed = g.Opp_Points_Scored AND s.Total_Yards = g.Total_Yards AND s.Yards_Per_Play = g.Yards_Per_Play;

-- -- Create the conversion_stats table
-- CREATE TABLE conversion_stats (
--     stat_id INT REFERENCES statline(stat_id),
--     Third_Down_Conversions INT,
--     Thirds_Down_Attempts INT,
--     Fourth_Down_Conversions INT,
--     Fourth_Down_Attempts INT
-- );

-- INSERT INTO conversion_stats(stat_id, Third_Down_Conversions, Thirds_Down_Attempts, Fourth_Down_Conversions, Fourth_Down_Attempts)
-- SELECT s.stat_id, g.Third_Down_Conversions, g.Thirds_Down_Attempts, g.Fourth_Down_Conversions, g.Fourth_Down_Attempts
-- FROM nfl_game_stats g
-- JOIN statline s ON s.Team_Full_Name = g.Team_Full_Name AND s.points_scored = g.Home_Points_Scored AND s.points_allowed = g.Opp_Points_Scored AND s.Total_Yards = g.Total_Yards AND s.Yards_Per_Play = g.Yards_Per_Play;

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

-- INSERT INTO kicking_stats(stat_id, Field_Goal_Attempts, Field_Goals_Made, Extra_Point_Attempts, Extra_Points_Made, Times_Punted, Total_Punt_Yards)
-- SELECT s.stat_id, g.Field_Goal_Attempts, g.Field_Goals_Made, g.Extra_Point_Attempts, g.Extra_Points_Made, g.Times_Punted, g.Total_Punt_Yards
-- FROM nfl_game_stats g
-- JOIN statline s ON s.Team_Full_Name = g.Team_Full_Name AND s.points_scored = g.Home_Points_Scored AND s.points_allowed = g.Opp_Points_Scored AND s.Total_Yards = g.Total_Yards AND s.Yards_Per_Play = g.Yards_Per_Play;