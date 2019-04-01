from Tkinter import *
from tkintertable import TableCanvas, TableModel
import pandas as pd

class interface:
	
	def __init__(self):

		root = Tk()

		root.title('NHL Elo Predictions')
		root.geometry('800x600')

		one = Label(root,text = 'NHL Elo Rankings', bg ='blue', fg = 'white')
		one.pack()

		tframe = Frame(root)
		tframe.pack()
		table = TableCanvas(tframe, rowheaderwidth=0,cellwidth=100,editable=False, width = 325)
		table.importCSV('team elos.csv')
		table.sortTable(columnName='elo', reverse = 1)
		colIndex = 1
		table.show()

		two = Label(root,text = 'Games Today', bg ='blue', fg = 'white')
		two.pack()

		tframe2 = Frame(root)
		tframe2.pack()
		table2 = TableCanvas(tframe2, rowheaderwidth=0,editable=False, width = 725)
		table2.importCSV('test.csv')
		table2.show()

		root.mainloop()


interface()

