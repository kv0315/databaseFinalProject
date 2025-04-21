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

NFL_Model_Visuals().barChart()
        
    