from Scraper import scraper
from eloCalc import eloCalc
from Tkinter import *
from tkintertable import TableCanvas, TableModel
from interface import interface


y = scraper(2017, 2019)

y.toCsv()

k = eloCalc()

k.toCsv()

k.upcomingGames()

interface()
