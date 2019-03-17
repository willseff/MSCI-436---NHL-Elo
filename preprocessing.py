import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("game outcomes.csv")

df.drop(labels=[ 'Att.', 'LOG', 'Notes'], inplace=True, axis=1)

le = LabelEncoder()

df[]

df.to_csv('game outcomes.csv')