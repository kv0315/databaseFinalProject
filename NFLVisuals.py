# from NFL_Model import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import time
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score, classification_report


class NFL_Model_Visuals:
    def __init__(self):
        self.NFL_df = pd.read_csv('nfl_data.csv')

        print(self.NFL_df)

NFL_Model_Visuals()
        
    