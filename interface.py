from Tkinter import *
from tkintertable import TableCanvas, TableModel

root = Tk()

tframe = Frame(root)
tframe.pack()
table = TableCanvas(tframe)
table.importCSV('team elos.csv')
table.show()

root.mainloop()

