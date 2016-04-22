import Tkinter
#import utils
#from qr import *
#from scanner import *
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

        # Set "Width x Height"
        self.geometry('800x480')

        # Add label under 'Next' Button
        nextLabel = Tkinter.Label(self, text = 'Place QR code in front of camera',)
        nextLabel.grid(column=0, row=1)

        nextBufferLabel = Tkinter.Label(self, text = '', height=10)
        nextBufferLabel.grid(column=0, row=2)

        nextLabel = Tkinter.Label(self, text = 'If qrcode not working or none present, input ubit name below')
        nextLabel.grid(column=0, row=3)

        # Add entry box for ubit names
        self.ubitEntryValue = Tkinter.StringVar()
        self.ubitEntry = Entry(self, cursor="xterm", exportselection=0)
        self.ubitEntry.grid(column=0, row=4)
        
        # Add 'Find' button
        self.findButton = Button(self, text="Find", command = self.get_name)
        self.findButton.grid(column=0, row=5)
        

        entryBufferLabel = Tkinter.Label(self, text = '', height=14)
        entryBufferLabel.grid(column=0, row=6)

        # Add connection status lable
        self.connectionLabelVariable = Tkinter.StringVar()
        self.connectionLabelVariable.set("Connected")

        self.connectionLabel = Label(self, textvariable=self.connectionLabelVariable, bg='#000fff000', height=1, width=20)
        self.connectionLabel.grid(column=0, row=7)

        self.cammeraSpacer = Tkinter.Label(self,text='',height=1)
        self.cammeraSpacer.grid(column=1,row=1)

    def get_name(self):
        name = self.ubitEntry.get()
        send_message(name)
        self.ubitEntry.delete(0,END)
    
                                  
















        
