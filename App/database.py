import pandas as pd
	
from scraper import game_data
from datetime import datetime
from peewee import *

# rename columns to better names
game_data.rename(columns={'G':'VisitingGoals',
                       	  'G.1':'HomeGoals',
                          'Unnamed: 5':'OTSO',
                          }, inplace = True)

# drop not needed information
game_data.drop(['Att.','LOG','Notes'], 
			    axis = 1, 
			    inplace=True)

# change date column to date type
game_data.loc[:,'Date'] = pd.to_datetime(game_data['Date'])

# replace names of teams that have changed location/name
replace_dict= {'Home':{'Atlanta Thrashers': 'Winnipeg Jets',
                      'Mighty Ducks of Anaheim': 'Anaheim Ducks',
                      'Phoenix Coyotes': 'Arizona Coyotes'},
              'Visitor':{'Atlanta Thrashers': 'Winnipeg Jets',
                      'Mighty Ducks of Anaheim': 'Anaheim Ducks',
                      'Phoenix Coyotes': 'Arizona Coyotes'}}

game_data.replace(replace_dict,inplace=True)

# change empty values in OTSO to display 'reg'
ind = game_data['OTSO'].isna()
game_data.loc[ind,'OTSO'] = 'REG'

# list of all the teams sorted
teams = game_data['Home'].unique()
teams.sort()

# functions to update the elos and return likelyhood of winning
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


# reset the index of the scraped data
games = game_data.reset_index()

# drop the index column
games.drop('index', axis=1, inplace=True)

# rename the season column to capitalize it
games.rename(columns={'season':'Season'}, inplace = True)

# for all the team elos store it in a class which inherits from dictionary
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


# create object
elos = TeamElos()
# itereate through the game data and update the teamelos object each time
for row in games.itertuples():
    if row.Date.date()< pd.Timestamp.today().date():
        elos.update(row)

# change the elos object to a dataframe and then sort the values
elos=pd.DataFrame(elos, index = ['Elo Rating']).T.sort_values(by='Elo Rating', ascending = False)

# select the games that have not happened yet
ind = games['Date'] >= pd.Timestamp('today')
games_future = games.loc[ind,:].reset_index()

# drop all the games that happened in the past
games_future.drop('index', axis=1, inplace=True)

# select first 10 games of the future games
games_prediction = games_future.loc[0:10,['Date', 'Visitor', 'Home']]

# merge the upcoming games with the elo ratings of the teams
games_prediction = games_prediction.merge(elos,left_on= 'Visitor', right_index = True)
# change the name of the column
games_prediction.rename(columns={'Elo Rating':'Visitor Elo Rating'
                       }, inplace = True)

# do the same thing for home teams
games_prediction = games_prediction.merge(elos,left_on= 'Home', right_index = True)
games_prediction.rename(columns={'Elo Rating':'Home Elo Rating'
                       }, inplace = True)

# use the expected result function to caculate the chance of winning
games_prediction['Home Win%']= expected_result(games_prediction['Home Elo Rating'],games_prediction['Visitor Elo Rating'])
games_prediction['Visitor Win%'] = 1-games_prediction['Home Win%']

# drop the elo ratings
games_prediction.drop(['Visitor Elo Rating','Home Elo Rating'], axis = 1, inplace=True)

# change order of the columns
games_prediction = games_prediction[['Date', 'Visitor', 'Visitor Win%','Home','Home Win%']]

db = SqliteDatabase('elos.db')

# prediction table with the next ten games being played and the percentage of winning
class Prediction(Model):
    date = DateField()
    visitor = CharField(max_length=50)
    visitor_win = FloatField(default=0)
    home = CharField(max_length=50)
    home_win = FloatField(default=0)
    class Meta:
        database = db

# table with all the elos of the teams        
class Elos(Model):
    team = CharField(max_length=50, unique=True)
    elo = FloatField(default=1500)
    class Meta:
        database = db
    
# function to take individual rows from the games_prediction df and input it into the db
def add_information_prediction(row):
    Prediction.create(date=row.Date,
				visitor=row.Visitor,
                visitor_win=row[3],
                home=row.Home,
                home_win=row[5]
                )

# # function to take individual rows from the elos series and input it into the db
def add_information_elos(tup):
    Elos.create(team=tup[0],
                elo=tup[1])
        
db.connect()
db.create_tables([Elos, Prediction], safe=True)

# iterate through the df and input data to the db
for row in games_prediction.itertuples():
    add_information_prediction(row)

# using zip to iterate because difficult to iterate over a pandas series
for row in zip(elos.index, map(float,elos.values)):
    add_information_elos(row)






