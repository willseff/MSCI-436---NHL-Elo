import pandas as pd
from datetime import datetime
from tkinter import *
from tkintertable import TableCanvas, TableModel

k_factor = 10
def update_elo(w_elo, l_elo):
    exp_win = expected_result(w_elo, l_elo)
    change = k_factor * (1-exp_win)
    w_elo = w_elo + change
    l_elo = l_elo - change
    return w_elo, l_elo

def expected_result(elo_a, elo_b):
    expect = 1.0/(1+10**((elo_b - elo_a)/400))
    return expect

df_lists = pd.DataFrame()
start_year= 2018
end_year = 2020

#scrapes data from hockeyreference.com
for year in range (start_year,end_year+1):
    k=1

    # 2005 was the lockout so there is no data to be scraped
    if year == 2005:
        print("2005 was the lockout")

    else:
        url = r'https://www.hockey-reference.com/leagues/NHL_' + str(year) + r'_games.html' 

        df_temp_reg = pd.DataFrame(pd.read_html(url)[0])
        df_temp_reg['season'] = year

    # use commented out code if playoff data is desired

        try:
            df_temp_post = pd.DataFrame(pd.read_html(url)[1])
            df_temp_post['season'] = year

        except IndexError as e:
            k = 0
            print('no playoffs available yet')
        
        print (str(year) + " scraped")

    df_lists = df_lists.append(df_temp_reg)

    if k == 1:
        df_lists.append(df_temp_post)


df_lists.rename(columns={'G':'VisitingGoals',
                       'G.1':'HomeGoals',
                       'Unnamed: 5':'OTSO',
                       }, inplace = True)

df_lists.drop(['Att.','LOG','Notes'], axis = 1, inplace=True)

df_lists.loc[:,'Date'] = pd.to_datetime(df_lists['Date'])

replace_dict= {'Home':{'Atlanta Thrashers': 'Winnipeg Jets',
                      'Mighty Ducks of Anaheim': 'Anaheim Ducks',
                      'Phoenix Coyotes': 'Arizona Coyotes'},
              'Visitor':{'Atlanta Thrashers': 'Winnipeg Jets',
                      'Mighty Ducks of Anaheim': 'Anaheim Ducks',
                      'Phoenix Coyotes': 'Arizona Coyotes'}}

df_lists.replace(replace_dict,inplace=True)

ind = df_lists['OTSO'].isna()
df_lists.loc[ind,'OTSO'] = 'REG'

# how come this doesnt work??? teams = df_lists['Home'].unique().sort()
teams = df_lists['Home'].unique()
teams.sort()

team_elos = {}
for team in teams:
    team_elos[team] = 1500
team_elos

games = df_lists.reset_index() 

games.drop('index', axis=1, inplace=True)

games.rename(columns={'season':'Season'}, inplace = True)

class TeamElos(dict):
    def __init__(self):
        super().__init__(self)
        for team in teams:
            self[team] = 1500
            
    def update(self, game_tuple):
        if game_tuple.VisitingGoals>game_tuple.HomeGoals:
            winning_team = game_tuple.Visitor
            losing_team = game_tuple.Home
        else:
            winning_team = game_tuple.Home
            losing_team = game_tuple.Visitor
        self[winning_team], self[losing_team] = update_elo(self[winning_team],self[losing_team])

elos = TeamElos()
for row in games.itertuples():
    if row.Date.date()< pd.Timestamp.today().date():
        elos.update(row)

elos=pd.DataFrame(elos, index = ['Elo Rating']).T.sort_values(by='Elo Rating', ascending = False)

ind = games['Date']> pd.Timestamp('today')

games_future = games.loc[ind,:].reset_index()
games_future.drop('index', axis=1, inplace=True)

games_prediction = games_future.loc[0:10,['Date', 'Visitor', 'Home']]

games_prediction = pd.DataFrame.merge(games_prediction,elos,left_on= 'Visitor', right_index = True)
games_prediction.rename(columns={'Elo Rating':'Visitor Elo Rating'
                       }, inplace = True)

games_prediction = pd.DataFrame.merge(games_prediction,elos,left_on= 'Home', right_index = True)
games_prediction.rename(columns={'Elo Rating':'Home Elo Rating'
                       }, inplace = True)

games_prediction['Home Win%']= expected_result(games_prediction['Home Elo Rating'],games_prediction['Visitor Elo Rating'])

games_prediction['Visitor Win%'] = 1-games_prediction['Home Win%']

games_prediction.drop(['Visitor Elo Rating','Home Elo Rating'], axis = 1, inplace=True)

games_prediction = games_prediction[['Date', 'Visitor', 'Visitor Win%','Home','Home Win%']]

elos.to_csv('elos.csv',index=True)
games_prediction.to_csv('prediction.csv', index = False)


root = Tk()

root.title('NHL Elo Predictions')
root.geometry('800x600')

one = Label(root,text = 'NHL Elo Rankings', bg ='blue', fg = 'white')
one.pack()

tframe = Frame(root)
tframe.pack()
table = TableCanvas(tframe, rowheaderwidth=0,cellwidth=100,editable=False, width = 325)
table.importCSV('elos.csv')
table.sortTable(columnName='Elo Rating', reverse = 1)
colIndex = 1
table.show()

two = Label(root,text = 'Games Today', bg ='blue', fg = 'white')
two.pack()

tframe2 = Frame(root)
tframe2.pack()
table2 = TableCanvas(tframe2, rowheaderwidth=0,editable=False, width = 725)
table2.importCSV('prediction.csv')
table2.show()

root.mainloop()



