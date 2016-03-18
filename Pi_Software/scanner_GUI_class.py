import Tkinter
import utils
from qr import *
from Tkinter import *

class Scanner_Window(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # Set Grid Layout, Non-resizable
        self.grid()
        self.resizable(False,False)

##        # Set Col Weights
##        self.columnconfigure(0, weight=1)
##        self.columnconfigure(1, weight=1)
##        self.columnconfigure(2, weight=1)
##
##        # Set Row Weights
##        for x in range(0,9):
##            self.rowconfigure(x,weight=1)

        # Set "Width x Height"
        self.geometry('400x480')

        # Add 'Next' button
        self.nextButton = Button(self,
                                    text="Next",
                                    height=3,
                                    width=10,
                                    state='normal',
                                    command=self.scanNext)
        self.nextButton.grid(column=0, row=0)

        # Add label under 'Next' Button
        nextLabel = Tkinter.Label(self,
                                  text = 'Press the "Next" button to scan next QR code',
                                  )
        nextLabel.grid(column=0, row=1)

        nextBufferLabel = Tkinter.Label(self,
                                        text = '',
                                        height=10
                                  )
        nextBufferLabel.grid(column=0, row=2)

        # Add entry box for ubit names
        self.ubitEntryValue = Tkinter.StringVar()
        self.ubitEntry = Entry(self,
                                  cursor="xterm",
                                  exportselection=0,
                                  state='disabled')
        self.ubitEntry.grid(column=0, row=3)
        
        # Add 'Find' button
        self.findButton = Button(self,
                                    text="Find",
                                 state='disabled')
        self.findButton.grid(column=0, row=4)
        
        # Add label under ubit entry
        entryLabel = Tkinter.Label(self,
                                    text = 'If QR code not working or not present, input ubit name above'
                                    )
        entryLabel.grid(column=0, row=5)

        entryBufferLabel = Tkinter.Label(self,
                                        text = '',
                                        height=10
                                  )
        entryBufferLabel.grid(column=0, row=6)

        # Add connection status lable
        self.connectionLabelVariable = Tkinter.StringVar()
        self.connectionLabelVariable.set("Connected")

        self.connectionLabel = Label(self,
                                        textvariable=self.connectionLabelVariable,
                                        bg='#000fff000',
                                        height=1,
                                        width=20)
        self.connectionLabel.grid(column=0, row=7)

    def scanNext(self):
        self.nextButton.config(state='disabled')
        self.update()
        self.ubitEntry.config(state='normal')
        self.update()
        self.findButton.config(state='normal')
        self.update()
        scan()
        self.nextButton.config(state='normal')
        self.update()        
    
                                  
















        
