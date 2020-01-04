from flask import Flask, render_template, redirect
from db_model import *
import pandas as pd

db = SqliteDatabase('elos.db')
db.connect()
# query db for the elos ratings
query = Elos.select()
# dict comprenshion!!!
elo_ratings = {row.team: row.elo for row in query}

# query db for the predictions
query = Prediction.select()
#list comprehension to turn query into list
predicts = [[row.id, 
             row.date, 
             row.visitor, 
             row.visitor_win, 
             row.home,
             row.home_win] for row in query]


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', 
							elo_ratings=elo_ratings)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/home')
def home():
	return redirect('/')

@app.route('/predictions')
def predictions():
	return render_template('predictions.html', 
						   predicts=predicts)

@app.route('/elohistory')
def elohistory():
	return('feature under construction')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8000)

