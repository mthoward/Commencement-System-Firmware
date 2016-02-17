import Tkinter
from sound_interface import *
from Tkinter import *
from utils import *


class Recording_Window(Tkinter.Tk):
   def __init__(self,parent):
      Tkinter.Tk.__init__(self,parent)
      self.parent = parent
      self.initialize()

   def initialize(self):
      # Set Grid Layout, Non-resizable
      self.grid()
      self.resizable(False,False)

      # Set Col Weights
      self.columnconfigure(0,weight=2)
      self.columnconfigure(1,weight=0)
      self.columnconfigure(2,weight=1)
      self.columnconfigure(3,weight=1)

      # Set Row Weights
      for x in range(0,9):
         self.rowconfigure(x,weight=1)

      # Set "Width x Height"
      self.geometry('400x200')


      #### Listbox
      self.listbox = Listbox(self)
      self.listbox.grid(row=0, column=0,
                        rowspan=9, columnspan=1,
                        padx=8,sticky='NSEW')
      self.listbox.columnconfigure(0,weight=1)
      for x in range(0,9):
         self.listbox.rowconfigure(x,weight=1)

      ### Scrollbar for Listbox
      self.scrollbar = Scrollbar(self.listbox, orient=VERTICAL)
      self.listbox.config(yscrollcommand=self.scrollbar.set)
      self.scrollbar.config(command=self.listbox.yview)
      self.scrollbar.grid(column=1, rowspan=9, sticky='NS')
      self.selection = self.listbox.get(ACTIVE)

      # Add '>>>' button
      self.listButtonVariable = Tkinter.StringVar()
      self.listButtonVariable.set(">>>")
      selButton = Tkinter.Button(self,
                              textvariable=self.listButtonVariable,
                              command=self.GetSelection)
      selButton.grid(column=1, row=3, padx=8)

      # Add Label Over Test Entry
      self.label = Label(self, text="UBIT NAME")
      self.label.grid(column=2, row=2, columnspan=2,padx=8)

      # Add Text Entry
      self.entryString = StringVar()
      self.entry = Tkinter.Entry(self, textvariable=self.entryString)
      self.entry.grid(column=2, row=3,
                      columnspan=2,
                      padx=8,
                      sticky='EW')
      self.entryString.set("")

      # Add record button
      self.buttonVariable = Tkinter.StringVar()
      self.buttonVariable.set(" Record ")
      button = Tkinter.Button(self,
                              textvariable=self.buttonVariable,
                              command=self.RecordPressed,
                              bg="white",
                              fg="red")
      button.grid(column=2, row=4, columnspan=1)

      # Add Playback button
      self.playbackVariable = Tkinter.StringVar()
      self.playbackVariable.set("Playback")
      button = Tkinter.Button(self,
                              textvariable=self.playbackVariable,
                              command=self.PlaybackPressed,
                              bg="white",
                              fg="blue")
      button.grid(column=3, row=4, columnspan=1)

      # Add Label Under Buttons
      self.statusLabel = Label(self, text='', fg="red")
      self.statusLabel.grid(column=2, row=5,
                             columnspan=2,padx=8)

   ## Returns the list selection
   def GetSelection(self):
      self.entryString.set(self.listbox.get(ACTIVE))


   ## Called when the Record button is pressed
   def RecordPressed(self):
      ## Change Button
      self.buttonVariable.set("Recording")
      self.update()

      ## Record Name
      UBIT = self.entryString.get().rstrip('\n')
      if UBIT == "":
         self.statusLabel.config(text="NO NAME SELECTED")
      else:
         self.statusLabel.config(text="Recording: '" + UBIT + ".wav'")
         self.update()
         record_wav_file(UBIT)
         self.statusLabel.config(text="")
         self.update()

      ## Refresh Button
      self.buttonVariable.set(" Record ")
      self.update()


   ## Called when the playback button is pressed
   def PlaybackPressed(self):
      ## Get UBIT
      UBIT = self.entryString.get().rstrip('\n')

      ## Error Checking
      if UBIT == "":
         self.statusLabel.config(text="NO NAME SELECTED")
         self.update()
      elif not check_file_exists(UBIT + ".wav"):
         self.statusLabel.config(text="NO RECORDING for '" + UBIT +"'")
         self.update()
      # Playback
      else:
         self.playbackVariable.set("Playing")
         self.statusLabel.config(text="Playing: '" + UBIT + ".wav'")
         self.update()

         ## Playback the UBIT file
         play_wav_file(UBIT + ".wav")

         ## Change GUI Back
         self.playbackVariable.set("Play")
         self.statusLabel.config(text="")
         self.update()
