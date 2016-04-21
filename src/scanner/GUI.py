""" scanner/GUI.py
"""

from Tkinter import Tk, Frame, Button, Label


class GUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.connectedLabel = Label(self)
        self.connectedLabel['text'] = 'Not connected'

        self.QUIT = Button(self)
        self.QUIT['text'] = 'Quit'
        self.QUIT['command'] =  self.quit
        self.QUIT.pack({'side': 'bottom'})

    def say_hi(self):
        print "hi there, everyone!"

root = Tk()
app = GUI(master=root)
app.mainloop()
root.destroy()
