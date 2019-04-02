import numpy as np 
import pandas as pd
from datetime import datetime

mean_elo = 1500
k_factor = 10

#method returns the new elos for two teams who plpay each other
def update_elo(w_elo, l_elo):
    exp_win = expected_result(w_elo, l_elo)
    change = k_factor * (1-exp_win)
    w_elo = w_elo + change
    l_elo = l_elo - change
    return w_elo, l_elo


#method returns the win probablities of two teams which are play one another
def expected_result(elo_a, elo_b):
    expect = 1.0/(1+10**((elo_b - elo_a)/400))
    return expect

 #method regresses elos for teams at the ends of each season
def update_end_of_season(elos):

    dif_from_mean = elos - mean_elo
    elos = elos - dif_from_mean/3
    return elos

df_reg = pd.read_csv("game outcomes.csv")

class eloCalc:

    def __init__ (self):

        df_reg = pd.read_csv("game outcomes.csv")

        df_reg['w_elo_after_game'] = 0
        df_reg['l_elo_after_game']  = 0

        data = [1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500]
        team_elos = pd.DataFrame(data)

        current_season = df_reg.at[0, 'season']
        for row in df_reg.itertuples():
            if row.season != current_season:
                # Check if we are starting a new season, if so then regress all ratings towards the mean
                team_elos = update_end_of_season(team_elos)
                current_season = row.season
                
            idx = row.Index
            if row.homeTeamGoals > -1 :
                if row.homeTeamGoals > row.visitorTeamGoals :
                    w_id = row.visitorTeamEncode
                    l_id = row.homeTeamEncode
                    
                else:
                    w_id = row.homeTeamEncode
                    l_id = row.visitorTeamEncode
                    
                # Get current elos
                w_elo_before = team_elos.iloc[w_id-1]
                l_elo_before = team_elos.iloc[l_id-1]
                # Update on game results
                w_elo_after, l_elo_after = update_elo(w_elo_before, l_elo_before)
                
                  # Save updated elos
                df_reg.at[idx, 'w_elo_after_game'] = w_elo_after
                df_reg.at[idx, 'l_elo_after_game'] = l_elo_after
                team_elos.iloc[w_id-1] = w_elo_after
                team_elos.iloc[l_id-1] = l_elo_after

            else:
                pass



        self.df_games = df_reg
        team_elos.columns = ['elo']
        team_elos['team'] = pd.read_csv('Team Encodings.csv')['Team']
        self.df_team_elos = team_elos


    #method to export game data and the elos of teams to csv format
    def toCsv(self):

        self.df_games.to_csv('out.csv', index = False)
        self.df_team_elos.to_csv('team elos.csv', index = False)

        print ('Elo results saved to csv')

    def upcomingGames(self):

        #change column to datetime
        self.df_games['Date'] = pd.to_datetime(self.df_games['Date'])
        #look for games which are occuring on today's date
        df_today = self.df_games.loc[self.df_games['Date'] == datetime.today().date()]
        count = 0

        # create two new empty columns
        df_today['homeTeam'] = ''
        df_today['visitorTeam'] = ''

        #lookup elo values of the teams playing today and calculate win percentages
        for row in df_today.itertuples():
            idx=row.Index
            count = count +1
            homeTeamElo = self.df_team_elos.iloc[row.homeTeamEncode-1][0]
            visitorTeamElo = self.df_team_elos.iloc[row.visitorTeamEncode-1][0]
            df_today.at[idx, 'homeTeamGoals'] = expected_result(homeTeamElo, visitorTeamElo)
            df_today.at[idx, 'visitorTeamGoals'] = 1-expected_result(homeTeamElo, visitorTeamElo)

            df_today.at[idx, 'homeTeam'] = str(self.df_team_elos.iloc[row.homeTeamEncode-1][1])
            df_today.at[idx, 'visitorTeam'] = str(self.df_team_elos.iloc[row.visitorTeamEncode-1][1])


        # output today's games as a table
        df_today = df_today.rename(columns = {"homeTeamGoals":"homeWinPercentage", "visitorTeamGoals": "visitorWinPercentage"})
        df_today = df_today[['Date', 'homeTeam', 'homeWinPercentage','visitorTeam', 'visitorWinPercentage']]

        df_today.to_csv('test.csv', index = False)

        print('todays predictions saved to csv')

        return df_today


