# pip install hockey scraper
import pandas as pd

df_lists = []

for year in range (2000,2010):

	if year == 2005:
		print("2005 was the lockout")

	else:
		url = r'https://www.hockey-reference.com/leagues/NHL_' + str(year) + r'_games.html' 

		df_lists.append(pd.read_html(url)[0])

		print (str(year) + " scraped")


df = pd.concat(df_lists)

df.to_csv('game outcomes.csv')


