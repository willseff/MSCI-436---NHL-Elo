# pip install hockey scraper
import pandas as pd
import datetime as dt

class scraper: 

	def __init__ (self,a,b):

		df_lists = []

		for year in range (a,b):

			if year == 2005:
				print("2005 was the lockout")

			else:
				url = r'https://www.hockey-reference.com/leagues/NHL_' + str(year) + r'_games.html' 

				df_lists.append(pd.read_html(url)[0])

				print (str(year) + " scraped")


		df = pd.concat(df_lists)
		teamEncodings = pd.read_csv('Team Encodings.csv')

		#df.drop(labels=[ 'Att.', 'LOG', 'Notes'], inplace=True, axis=1)

		df['homeTeamEncode'] = 0
		df['visitorTeamEncode'] = 0

		df['Date'] = pd.to_datetime(df['Date'])


		for gameRow in df.itertuples():
			for teamRow in teamEncodings.itertuples():
				if gameRow.Visitor == teamRow.Team:

					idx = gameRow.Index

					df.at[idx, 'visitorTeamEncode'] = teamRow.Encoding

		print('Visiting Teams Encoded')			

		for gameRow in df.itertuples():
			for teamRow in teamEncodings.itertuples():
				if gameRow.Home == teamRow.Team:

					idx = gameRow.Index

					df.at[idx, 'homeTeamEncode'] = teamRow.Encoding

		print('Home Teams Encoded')			


		self.df = df [['Date','homeTeamEncode', 'G','visitorTeamEncode', 'G.1', 'Unnamed: 5']]



	def toCsv(self):

		self.df.to_csv('game outcomes.csv')

	def returnDf(self):

		return self.df




