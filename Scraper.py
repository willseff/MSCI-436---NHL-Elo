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

		self.df = pd.concat(df_lists)



	def toCsv(self):

		self.df.to_csv('game outcomes.csv')

	def returnDf(self):

		return self.df




