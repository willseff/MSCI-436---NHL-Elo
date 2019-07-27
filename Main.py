from Scraper import scraper
from eloCalc import eloCalc
from tkinter import *
from tkintertable import TableCanvas, TableModel
from interface import interface

#create scraper object
y = scraper(2017, 2019)

# output data to csv
y.toCsv()

#create eloCalc object
k = eloCalc()

#output caculated data to csv
k.toCsv()

#output table to todays games to csv
k.upcomingGames()

#build interface
interface()
