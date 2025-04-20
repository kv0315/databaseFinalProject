Kaden Valdez
Aedon Kettles
Component 1: 


Component 3: 
- Your choice (Data Scraping and Cleaning Using Python):
Used 'https://www.pro-football-reference.com/teams/' + {team} + '/' + {season} + '/gamelog/' for every team from 2010 to 2024 to get every game for each team into a dataframe where we would remove incomplete rows, and the season totals row. We would then clean the column names of the data 
for better read ability because the names are not descriptive. For example the column "Unnamed: 5" correlated to whether that specific game was played at home or away. We also altered the values of the columns "Home", "Result", and "OT" to be binary, so if a team was at Home the corresponding value would be a 1, and away would be a 0. For result a value of 1 would be a win, and a loss would be a 0, finally for the OT (overtime) column a value of 1 says the game went to overtime, and a value 0 says it did not go into overtime. We would also add a column that would add both teams in the games full name rather than just both of their 3 letter abreviations. 