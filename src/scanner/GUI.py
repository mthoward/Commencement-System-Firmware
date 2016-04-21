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
        self.connectedLabel.pack({'side': 'top'})

        self.

        self.quitButton = Button(self)
        self.quitButton['text'] = 'Quit'
        self.quitButton['command'] =  self.quit
        self.quitButton.pack({'side': 'bottom'})

root = Tk()
app = GUI(master=root)
app.mainloop()
root.destroy()
