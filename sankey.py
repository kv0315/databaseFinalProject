import pandas as pd
import plotly.graph_objects as go

# Load data
df = pd.read_csv('nfl_data.csv')

# Keep all teams now (no filtering)
df = df[df['Game_Result'].isin(['W', 'L'])]  # Still remove ties

# Create categories
df['Home/Away'] = df['is_Home'].map({1: 'Home', 0: 'Away'})
df['Turnover_Bucket'] = df['Turnovers'].apply(lambda x: '0 Turnovers' if x == 0 else ('1 Turnover' if x == 1 else '2+ Turnovers'))
df['Scoring_Category'] = df['Home_Points_Scored'].apply(lambda x: '30+ Points' if x >= 30 else '<30 Points')

# Create nodes
teams = df['Team_Full_Name'].unique().tolist()
homeaway = ['Home', 'Away']
scoring = ['30+ Points', '<30 Points']
turnovers = ['0 Turnovers', '1 Turnover', '2+ Turnovers']
results = ['W', 'L']

all_nodes = teams + homeaway + scoring + turnovers + results
node_indices = {label: idx for idx, label in enumerate(all_nodes)}

# Create flows
def add_flow(df, src, tgt):
    group = df.groupby([src, tgt]).size().reset_index(name='count')
    s = group[src].map(node_indices)
    t = group[tgt].map(node_indices)
    v = group['count']
    return list(s), list(t), list(v)

source, target, value = [], [], []
flow_pairs = [
    ('Team_Full_Name', 'Home/Away'),
    ('Home/Away', 'Scoring_Category'),
    ('Scoring_Category', 'Turnover_Bucket'),
    ('Turnover_Bucket', 'Game_Result')
]

for src, tgt in flow_pairs:
    s, t, v = add_flow(df, src, tgt)
    source += s
    target += t
    value += v

# Real NFL team colors (for 10 teams only)
team_colors_map = {
    'Miami Dolphins': '#008E97',
    'Kansas City Chiefs': '#E31837',
    'Green Bay Packers': '#203731',
    'Denver Broncos': '#FB4F14',
    'Minnesota Vikings': '#4F2683',
    'Los Angeles Rams': '#003594',
    'Las Vegas Raiders': '#A5ACAF',
    'Jacksonville Jaguars': '#006778',
    'Tampa Bay Buccaneers': '#D50A0A',
    'Baltimore Ravens': '#241773'
}

# If a team is not in the color map, use a default color
default_team_color = "#888888"  # soft gray for unknown teams
colors = [team_colors_map.get(t, default_team_color) for t in teams] + [
    '#FFD580', '#80BFFF',  # Home/Away soft
    '#CCFFCC', '#FFCCCC',  # Scoring soft
    '#CCE5FF', '#FFE599', '#E0BBE4',  # Turnover buckets
    '#99FF99', '#FF9999'   # Win/Loss
]

# Build Sankey
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_nodes,
        color=colors,
        font=dict(color="black", size=12)  # ✅ Add this line for darker text!

    ),
    link=dict(
        source=source,
        target=target,
        value=value
    )
)])

fig.update_layout(title_text="All NFL Teams → Home/Away → Scoring → Turnover → Result", font_size=10, width=1600, height=900)
fig.show()
