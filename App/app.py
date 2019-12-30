from flask import Flask, render_template 
from db_model import *

db = SqliteDatabase('elos.db')
db.connect()
query = Elos.select()
# dict comprenshion!!!
elo_ratings = {row.team: row.elo for row in query}

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', elo_ratings=elo_ratings)

app.run(debug=True, host='0.0.0.0', port=8000)


