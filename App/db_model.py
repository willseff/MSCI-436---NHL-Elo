from peewee import *

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

query = Elos.select()

# dict comprenshion!!!
elo_ratings = {row.team: row.elo for row in query}


