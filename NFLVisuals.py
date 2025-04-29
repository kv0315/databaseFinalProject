# from NFL_Model import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import time
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score, classification_report


class NFL_Model_Visuals:
    def __init__(self):
        self.NFL_df = pd.read_csv('nfl_data.csv')


    def barChart(self):
        game_results = self.NFL_df[['Team_Full_Name', 'Opp_Full_Name', 'Game_Result']]
        teams_records = game_results.groupby(['Team_Full_Name', 'Game_Result']).size().unstack(fill_value=0)
        teams_records = teams_records.rename(columns={'W': 'Wins', 'L': 'Losses', 'T':'Ties'})
        
        # Plot
        teams_records[['Wins', 'Losses', 'Ties']].plot(kind='bar', stacked=True, figsize=(12, 6))
        plt.title("NFL Team Win/Loss Records")
        plt.ylabel("Number of Games")
        plt.xlabel("Team")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()
    
    def lineChart(self):
        yearly_sum = self.NFL_df.groupby('Season')
        for year in yearly_sum:
            penalty_yards = yearly_sum['Penalty_Yards'].sum() / yearly_sum.size()
            turnovers = yearly_sum['Turnovers'].sum() / yearly_sum.size()
            total_games = yearly_sum.size()
            # print(round(rushing_total / total_games, 2))
            # print(round(penalty_yards / total_games, 2))
            print(turnovers)
        season = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
        passing_yards = [221.55, 229.69, 231.29, 235.60, 236.81, 243.82, 241.48, 224.36, 237.77, 234.96, 240.15, 228.31, 218.52, 218.92, 217.62]
        rushing_yards = [114.47, 117.14, 115.92, 112.88, 111.33, 108.84, 108.91, 109.71, 114.46, 112.90, 118.88, 115.25, 121.58, 112.66, 119.81]
        plt.plot(season, penalty_yards, color='red', linestyle='--', marker='o')
        plt.plot(season, turnovers, color='blue', marker='o')
        # plt.show()

NFL_Model_Visuals().snakey()
        
    