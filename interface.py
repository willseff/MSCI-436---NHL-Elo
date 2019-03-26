from Tkinter import *
from tkintertable import TableCanvas, TableModel

root = Tk()

one = Label(root,text = 'NHL Elo', bg ='blue', fg = 'white')
one.pack()

tframe = Frame(root)
tframe.pack()
table = TableCanvas(tframe, rowheaderwidth=0)
table.importCSV('team elos.csv')
table.show()

two = Label(root,text = 'Upcoming Games', bg ='blue', fg = 'white')
two.pack()

#make a df with upcoming games and chance of win here

root.mainloop()

