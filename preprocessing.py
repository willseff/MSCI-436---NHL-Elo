import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("game outcomes.csv")
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


for gameRow in df.itertuples():
	for teamRow in teamEncodings.itertuples():
		if gameRow.Home == teamRow.Team:

			idx = gameRow.Index

			df.at[idx, 'homeTeamEncode'] = teamRow.Encoding


df = df [['Date','homeTeamEncode', 'G','visitorTeamEncode', 'G.1', 'Unnamed: 5']]



df.to_csv('game outcomes.csv')