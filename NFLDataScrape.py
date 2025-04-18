import numpy as np
import pandas as pd
import random
import time

# Maps the 3-Letter Abr to the Full Name
abbrev_to_name = {
    'CRD': 'Arizona Cardinals', 'ARI': 'Arizona Cardinals', 'ATL':'Atlanta Falcons', 'RAV': 'Baltimore Ravens', 'BAL':'Baltimore Ravens', 'BUF':'Buffalo Bills',
    'CAR':'Carolina Panthers', 'CHI':'Chicago Bears', 'CIN':'Cincinnati Bengals', 'CLE':'Cleveland Browns', 'DAL':'Dallas Cowboys', 'DEN':'Denver Broncos', 
    'DET':'Detriot Lions', 'GNB':'Green Bay Packers', 'HTX':'Houston Texans', 'HOU':'Houston Texans', 'CLT':'Indianapolis Colts', 'IND':'Indianapolis Colts',
    'JAX':'Jacksonville Jaguars', 'KAN':'Kansas City Chiefs', 'SDG':'Los Angeles Chargers', 'LAC':'Los Angeles Chargers', 'RAM':'Los Angeles Rams', 'LAR':'Los Angeles Rams',
    'RAI':'Los Vegas Raiders', 'LVR':'Los Vegas Raiders', 'MIA':'Miami Dolphins', 'MIN':'Minnesota Vikings', 'NWE': 'New England Patriots', 'NOR':'New Orleans Saints',
    'NYG':'New York Giants', 'NYJ':'New York Jets', 'PHI':'Philadelphia Eagles', 'PIT': 'Pittsburgh Steelers', 'SFO':'San Francisco 49ers', 'SEA':'Seattle Seahawks', 'TAM':'Tampa Bay Buccaneers',
    'OTI':'Tennessee Titans', 'TEN':'Tennessee Titans', 'WAS':'Washington Commanders'
}

# Map Any 3 Letter Abreviation to Our Desired Abreviations
correct_abr = {
    'CRD': 'ARI', 'HTX': 'HOU', 'CLT': 'IND', 'SDG': 'LAC', 'RAM': 'LAR', 'RAI': 'LVR', 'OTI':'TEN', 'RAV': 'BAL',
}

 # Teams 3 Letter Abreviation Accoring to PFF Website
teams = [
    'crd', 'atl', 'rav', 'buf', 'car', 'chi', 'cin', 'cle', 'dal', 'den', 'det', 'gnb', 'htx', 'clt', 'jax', 'kan', 
     'sdg', 'ram', 'rai', 'mia', 'min', 'nwe', 'nor', 'nyg', 'nyj', 'phi', 'pit', 'sea', 'sfo', 'tam', 'oti', 'was']

class nfl_scrape:
    def __init__(self):
        # Each Season we want to include data from range(Start_Year(Includes), End_Year(Excludes))
        self.seasons = [str(season) for season in range(2010, 2025)]

        # Contains Gamelog Data and Vegas Lines Data
        self.nfl_df = pd.DataFrame()
        self.vegas_df = pd.DataFrame()

        # Contain the current season and current week of that season
        self.current_season = None
        self.current_week = None


    # Get Each Teams Weekly Game Logs From Each Season 
    def download_gamelogs(self):
        for season in self.seasons:
            for team in teams:
                # Set the URL for each of the teams for each of the seasons
                url = 'https://www.pro-football-reference.com/teams/' + team + '/' + season + '/gamelog/'
                print(f"Getting URL:  {url}")

                # Get the Results For Each Team
                curr_team_df = pd.read_html(url, header=1)[0]

                # Insert Season as New Column
                curr_team_df.insert(loc=0, column='Season', value=season)

                # Insert Team as New Column
                curr_team_df.insert(loc=2, column='Team_Abr', value=team.upper())

                # Add the Teams Gamelogs to the Rest of the Gamelogs Gathered
                self.nfl_df = pd.concat([self.nfl_df, curr_team_df], ignore_index=True)

                # Rest Time to Avoid Time Out From Accessing Data
                time.sleep(random.randint(7, 8))

            # Keep Track of Current Season
            self.current_season = season

        # Save the Data to a CSV File
        self.nfl_df.to_csv('databaseFinalProject/nfl_data.csv', index=False)

    def clean_gamelogs(self):
        # Read in content from the Game Logs
        self.nfl_df = pd.read_csv('databaseFinalProject/nfl_data.csv')

        # Remove unneeded Columns
        if (self.nfl_df.shape[1] == 50):
            self.nfl_df = self.nfl_df.drop(self.nfl_df.columns[1], axis=1)    # Removes RK column
            self.nfl_df = self.nfl_df.drop(self.nfl_df.columns[2], axis=1)    # Removes the Gtm Column
            self.nfl_df = self.nfl_df.drop(self.nfl_df.columns[4], axis=1)    # Removes the day column

        # Remove the Seasons Total Stats
        if 'Opp' in self.nfl_df.columns:
            self.nfl_df = self.nfl_df.dropna(subset=['Opp'])

        # # Rename Columns for easier readability
        column_names = {'Unnamed: 5': 'Home', 'Rslt':'Result', 'Cmp%': 'Completion_Percentage',
                        'Yds':'Pass_Yards', 'TD':'Pass_TD', 'Y/A':'Pass_YPA', 'AY/A':'Adjusted_YPA', 'Rate': 'Passer_Rating', 'Sk':'Sacks_Taken', 'Yds.1':'Sack_Yards', 
                        'Att.1':'Rush_Attempts', 'Yds.2':'Rush_Yards', 'TD.1':'Rush_TD', 'Y/A.1':'Rush_YPA', 
                        'Ply':'Total_Offensive_Plays', 'Tot':'Total_Yards', 'Y/P': 'Yards_Per_Play', 
                        'FL':'Fumbles_Lost', 'Int':'Interceptions_Thrown', 'TO':'Turnovers', 'ToP':'Time_Of_Posession'}
        self.nfl_df = self.nfl_df.rename(columns=column_names)

        # Add the full team name before the Team, and Opp Columns
        if 'Home_Full_Name' not in self.nfl_df.columns:
            self.nfl_df.insert(loc=1, column='Home_Full_Name', value=self.nfl_df['Team'].replace(abbrev_to_name))
        if 'Away_Full_Name' not in self.nfl_df.columns:
            self.nfl_df.insert(loc=6, column='Away_Full_Name', value=self.nfl_df['Opp'].replace(abbrev_to_name))

        # If Current Team Won the Result columm will display a 1
        self.nfl_df['Result'] = self.nfl_df['Result'].apply(lambda x: 1 if x == 'W' else 0)

        # If the Game went into OT then OT Column will display a 1
        self.nfl_df['OT'] = self.nfl_df['OT'].apply(lambda x: 1 if x == 'OT' else 0)

        # If the Current Team was the Home Team the Home Column will display a 1
        self.nfl_df['Home'] = self.nfl_df['Home'].apply(lambda x: 0 if x == '@' else 1)

        # Correct the Team, and Opp Column Values to Correct Abreviation
        if 'Team' in self.nfl_df.columns:
            self.nfl_df = self.nfl_df.rename(columns={'Team': 'Home_Team_Abr'})
        if 'Opp' in self.nfl_df.columns:
            self.nfl_df = self.nfl_df.rename(columns={'Opp': 'Away_Team_Abr'})

        self.nfl_df['Home_Team_Abr']= self.nfl_df['Home_Team_Abr'].replace(correct_abr)
        self.nfl_df['Away_Team_Abr'] = self.nfl_df['Away_Team_Abr'].replace(correct_abr)


        # Save Cleaned Data Back Into the CSV File
        self.nfl_df.to_csv('databaseFinalProject/nfl_data.csv', index=False)

nfl = nfl_scrape()
nfl.download_gamelogs()
# nfl.clean_gamelogs()