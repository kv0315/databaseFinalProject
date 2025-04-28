import pandas as pd
import plotly.graph_objects as go

# Step 1: Load your cleaned data
df = pd.read_csv('nfl_data.csv')

# Step 2: Create a Turnover Category
def turnover_bucket(turnovers):
    if turnovers == 0:
        return '0 Turnovers'
    elif turnovers == 1:
        return '1 Turnover'
    else:
        return '2+ Turnovers'

df['Turnover_Bucket'] = df['Turnovers'].apply(turnover_bucket)

# Step 3: Create the links for the Sankey
# Sources: Teams -> Game Results -> Turnover Buckets
teams = df['Team_Full_Name'].unique().tolist()
results = ['W', 'L', 'T']  # win, loss, tie
turnover_buckets = ['0 Turnovers', '1 Turnover', '2+ Turnovers']

# Create all node labels
all_nodes = teams + results + turnover_buckets

# Mapping each node to an index
node_indices = {label: idx for idx, label in enumerate(all_nodes)}

# Create source/target/values lists
source = []
target = []
value = []

# Step 4: First layer: Team → Game Result
team_result_group = df.groupby(['Team_Full_Name', 'Game_Result']).size().reset_index(name='count')

for _, row in team_result_group.iterrows():
    source.append(node_indices[row['Team_Full_Name']])
    target.append(node_indices[row['Game_Result']])
    value.append(row['count'])

# Step 5: Second layer: Game Result → Turnover Bucket
result_turnover_group = df.groupby(['Game_Result', 'Turnover_Bucket']).size().reset_index(name='count')

for _, row in result_turnover_group.iterrows():
    source.append(node_indices[row['Game_Result']])
    target.append(node_indices[row['Turnover_Bucket']])
    value.append(row['count'])

# Step 6: Build the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_nodes,
        color="blue"
    ),
    link=dict(
        source=source,
        target=target,
        value=value
    ))])

fig.update_layout(title_text="NFL Team → Game Result → Turnover Bucket (2010–2024)", font_size=10)
fig.show()
