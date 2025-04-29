import pandas as pd
import plotly.express as px

# Load your data
df = pd.read_csv('nfl_data.csv')

# Create turnover bucket
def turnover_bucket(turnovers):
    if turnovers == 0:
        return '0 Turnovers'
    elif turnovers == 1:
        return '1 Turnover'
    else:
        return '2+ Turnovers'

df['Turnover_Bucket'] = df['Turnovers'].apply(turnover_bucket)
df['Home/Away'] = df['is_Home'].map({1: 'Home', 0: 'Away'})

# Create TD Comparison Category
def td_type(row):
    if row['Pass_TD'] > row['Rush_TD']:
        return 'More Pass TDs'
    elif row['Rush_TD'] > row['Pass_TD']:
        return 'More Rush TDs'
    else:
        return 'Equal Pass/Rush TDs'

df['TD_Comparison'] = df.apply(td_type, axis=1)

# Filter for selected teams
selected_teams = ['Denver Broncos', 'Kansas City Chiefs', 'Green Bay Packers']
df_small = df[df['Team_Full_Name'].isin(selected_teams)]

# filter out ties
df_small = df_small[df_small['Game_Result'].isin(['W', 'L'])]

# Group data and create counts
grouped = df_small.groupby(['Team_Full_Name', 'Home/Away', 'Game_Result', 'TD_Comparison']).size().reset_index(name='count')

# label the data
grouped['Game_Result_Label'] = grouped['Game_Result'] + ' (' + grouped.groupby(['Team_Full_Name', 'Home/Away', 'Game_Result'])['count'].transform('sum').astype(str) + ')'
grouped['TD_Comparison_Label'] = grouped['TD_Comparison'] + ' (' + grouped['count'].astype(str) + ')'

# Build the sunburst
fig = px.sunburst(
    grouped,
    path=['Team_Full_Name', 'Home/Away', 'Game_Result_Label', 'TD_Comparison_Label'],
    values='count',
    color='Game_Result',
    color_discrete_map={
        'W': 'green',
        'L': 'red'
    },
    title="Selected NFL Teams: Home/Away → Wins/Losses (count) → TD Type (count)",
    width=900,
    height=900
)

fig.show()
