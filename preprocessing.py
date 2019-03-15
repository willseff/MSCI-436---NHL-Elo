import pandas as pd

df = pd.read_csv("game outcomes.csv")

df.drop(labels=[ 'Att.', 'LOG', 'Notes'], inplace=True, axis=1)

df.to_csv('game outcomes.csv')