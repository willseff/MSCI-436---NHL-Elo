import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from datetime import datetime


sns.set_style("darkgrid")
sns.set_context("notebook")

def update_elo(winner_elo, loser_elo):
    """
    https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details
    """
    expected_win = expected_result(winner_elo, loser_elo)
    change_in_elo = k_factor * (1-expected_win)
    winner_elo += change_in_elo
    loser_elo -= change_in_elo
    return winner_elo, loser_elo
def expected_result(elo_a, elo_b):
    """
    https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details
    """
    expect_a = 1.0/(1+10**((elo_b - elo_a)/elo_width))
    return expect_a
def update_end_of_season(elos):
    """Regression towards the mean
    
    Following 538 nfl methods
    https://fivethirtyeight.com/datalab/nfl-elo-ratings-are-back/
    """
    diff_from_mean = elos - mean_elo
    elos -= diff_from_mean/3
    return elos

df_reg = pd.read_csv("game.csv")
for row in df_reg.itertuples():
    idx = row.Index

    s = df_reg.at[idx,'date_time']

df_reg.drop(labels=[ 'home_rink_side_start', 'venue', 'venue_link', 'venue_time_zone_id','venue_time_zone_offset','venue_time_zone_tz'], inplace=True, axis=1)
df_reg.sort_values(by=['date_time'], inplace=True)
df_reg.head()
mean_elo = 1500
elo_width = 400
k_factor = 64

df_reg['w_elo_after_game'] = 0

df_reg['l_elo_after_game'] = 0
data = [1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500]
team_elos = pd.DataFrame(data)
print(team_elos.iloc[6])
current_season = df_reg.at[0, 'season']
for row in df_reg.itertuples():
    if row.season != current_season:
        # Check if we are starting a new season. 
        # Regress all ratings towards the mean
        team_elos = update_end_of_season(team_elos)
        # Write the beginning of new season ratings to a dict for later lookups.
        current_season = row.season
        
    idx = row.Index
    if row.outcome == 'away win REG' or 'away win OT':
        w_id = row.away_team_id-1
        l_id = row.home_team_id-1
        
    elif row.outcome == 'home win REG' or 'home win OT':
        w_id = row.home_team_id-1
        l_id = row.away_team_id-1
        
    # Get current elos
    w_elo_before = team_elos.iloc[w_id]
    l_elo_before = team_elos.iloc[l_id]
    # Update on game results
    w_elo_after, l_elo_after = update_elo(w_elo_before, l_elo_before)
    
      # Save updated elos
    df_reg.at[idx, 'w_elo_after_game'] = w_elo_after
    df_reg.at[idx, 'l_elo_after_game'] = l_elo_after
    team_elos.iloc[w_id] = w_elo_after
    team_elos.iloc[l_id] = l_elo_after


df_reg.to_csv('out.csv')


