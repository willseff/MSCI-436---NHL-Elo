import pandas as pd
import datetime as dt

#this class scrapes game data from hockeyreference.com and reformats it into a more usable format.
class scraper: 

	def __init__ (self,a,b):

		df_lists = []

		#scrapes data from hockeyreference.com
		for year in range (a,b+1):
			k=1

			# 2005 was the lockout so there is no data to be scraped
			if year == 2005:
				print("2005 was the lockout")

			else:
				url = r'https://www.hockey-reference.com/leagues/NHL_' + str(year) + r'_games.html' 

				df_temp_reg = pd.DataFrame(pd.read_html(url)[0])
				df_temp_reg['season'] = year

				#try:
					#df_temp_post = pd.DataFrame(pd.read_html(url)[1])
					#df_temp_post['season'] = year

				#except IndexError as e:
					#k = 0
				 	#print('no playoffs available yet')


				df_lists.append(df_temp_reg)

				#if k == 1:
					#df_lists.append(df_temp_post)

				print (str(year) + " scraped")


		df = pd.concat(df_lists)
		teamEncodings = pd.read_csv('Team Encodings.csv')

		#df.drop(labels=[ 'Att.', 'LOG', 'Notes'], inplace=True, axis=1)

		# creates two new columns to turn the team names into numerical encodings
		df['homeTeamEncode'] = 0
		df['visitorTeamEncode'] = 0

		#turn date column from string to datetime object
		df['Date'] = pd.to_datetime(df['Date'])

		#iterates through each row in the dataframe and crossreferences it to the appopriate encoding from a csv dictionary of values
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


		df_temp = df [['Date','homeTeamEncode', 'G','visitorTeamEncode', 'G.1', 'Unnamed: 5','season']]
		df_temp = df_temp.rename(columns = {'G': 'homeTeamGoals', 'G.1': 'visitorTeamGoals'})

		self.df = df_temp


	# method exports the dataframe to csv format
	def toCsv(self):

		self.df.to_csv('game outcomes.csv')

		print("game outcomes saved to CSV")

	#method returns the dataframe
	def returnDf(self):

		return self.df




