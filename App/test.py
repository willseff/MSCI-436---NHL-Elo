from peewee import *
import pandas as pd


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

db.connect()

#query = Elos.select()

#print({row.team: row.elo for row in query})

query = Prediction.select()
#list comprehension to turn query into list
prediction = [[row.id, 
               row.date, 
               row.visitor, 
               row.visitor_win, 
               row.home,
               row.home_win] for row in query]

# then turn list in to df
df = pd.DataFrame(prediction)

for row in df.itertuples():
    print(row[0])



