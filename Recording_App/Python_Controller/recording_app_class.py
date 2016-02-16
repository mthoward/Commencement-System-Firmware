import Tkinter
from sound_interface import *
from Tkinter import *
import ttk
import threading, time
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
      self.columnconfigure(0,weight=1, minsize=100)
      self.columnconfigure(1,weight=1)
      self.columnconfigure(2,weight=1)
      self.columnconfigure(3,weight=1)
      self.columnconfigure(4,weight=1)

      # Set Row Weights
      for x in range(0,9):
         self.rowconfigure(x,weight=1)

      # Set "Width x Height"
      self.geometry('500x200')


      #### UBITListbox
      self.UBITListbox = Listbox(self)
      self.UBITListbox.grid(row=0, column=0,
                        rowspan=9,
                        padx=8,sticky='NSEW')
      self.UBITListbox.columnconfigure(0,weight=1)
      for x in range(0,9):
         self.UBITListbox.rowconfigure(x,weight=1)
      

      self.StatusListbox = Listbox(self)
      self.StatusListbox.grid(row=0, column=1,
                        rowspan=9,sticky='NSEW')
      self.StatusListbox.columnconfigure(0,weight=1)
      for x in range(0,9):
         self.StatusListbox.rowconfigure(x,weight=1)
         
         

      ### Scrollbar for UBITListbox
      self.scrollbar = Scrollbar(self.UBITListbox,
                                 orient=VERTICAL,
                                 command=self.OnVsb)
      self.UBITListbox.config(yscrollcommand=self.scrollbar.set,
                              activestyle=NONE)
      self.StatusListbox.config(yscrollcommand=self.scrollbar.set,
                                width=7,
                                exportselection=0,
                                activestyle=NONE)
      self.scrollbar.grid(column=1, rowspan=9, sticky='NS')
      self.selection = self.UBITListbox.get(ACTIVE)

      # Add '>>>' button
      self.listButtonVariable = Tkinter.StringVar()
      self.listButtonVariable.set(">>>")
      selButton = Tkinter.Button(self,
                                 textvariable=self.listButtonVariable,
                                 command=self.GetSelection)
      selButton.grid(column=2, row=3, padx=8)

      # Add Label Over Test Entry
      self.label = Label(self, text="UBIT NAME")
      self.label.grid(column=2, row=2, columnspan=2,padx=8)

      # Add Text Entry
      self.entryString = StringVar()
      self.entry = Tkinter.Entry(self, textvariable=self.entryString)
      self.entry.grid(column=3, row=3,
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
      button.grid(column=3, row=4, columnspan=1)

      # Add Playback button
      self.playbackVariable = Tkinter.StringVar()
      self.playbackVariable.set("Playback")
      button = Tkinter.Button(self,
                              textvariable=self.playbackVariable,
                              command=self.PlaybackPressed,
                              bg="white",
                              fg="blue")
      button.grid(column=4, row=4, columnspan=1)

      # Add Label Under Buttons
      self.statusLabel = Label(self, text='', fg="red")
      self.statusLabel.grid(column=3, row=5,
                             columnspan=2,padx=8)
      
      
      # Add Progressbar
      self.barStyle = ttk.Style()
      self.barStyle.theme_use('clam')
      self.barStyle.configure("red.Horizontal.TProgressbar", foreground="red", background="red")
      self.barVariable = Tkinter.IntVar()
      self.bar = ttk.Progressbar(self,
                                 orient=HORIZONTAL,
                                 length=200,
                                 mode='determinate',
                                 maximum=30,
                                 variable = self.barVariable,
                                 style="red.Horizontal.TProgressbar")
      self.bar.grid(column=3, row=7)
      
   ## Returns the list selection
   def GetSelection(self):
      self.entryString.set(self.UBITListbox.get(ACTIVE))


   ## Called when the Record button is pressed
   def RecordPressed(self):
      ## Change Button
      self.buttonVariable.set("Recording")
      self.barVariable.set(0)
      self.update()
      self.thread2 = threading.Thread(target=self.progress_bar_updater)
      self.thread2.start()

      ## Record Name
      UBIT = self.entryString.get().rstrip('\n')
      if UBIT == "":
         self.statusLabel.config(text="NO NAME SELECTED")
      else:
         self.statusLabel.config(text="Recording: '" + UBIT + ".wav'")
         self.bar.start()
         self.update()
         record_wav_file(UBIT)
         self.statusLabel.config(text="")
         self.update_listbox_entry()
         self.update()
         self.bar.stop()
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
      ## Playback
      else:
         self.playbackVariable.set("Playing ")
         self.statusLabel.config(text="Playing: '" + UBIT + ".wav'")
         self.update()

         ## Playback the UBIT file
         play_wav_file(UBIT + ".wav")

         ## Change GUI Back
         self.playbackVariable.set("Playback")
         self.statusLabel.config(text="")
         self.update()
   
   def progress_bar_updater(self):
      x = 0
      while x < 30:
         time.sleep(0.1)
         self.barVariable.set(x)
         self.update()
         x += 1
      self.barVariable.set(0)
      self.update()
   
   ## This allows Listboxes to share same scrolling
   def OnVsb(self, *args):
      self.UBITListbox.yview(*args)
      self.StatusListbox.yview(*args)
   
   ## This updates listbox 
   def update_listbox_entry(self):
      found = False
      x = 0
      while((not found) and (x<self.StatusListbox.index(END)+1)):
         if ''.join(self.UBITListbox.get(x,x)).rstrip() == self.entryString.get().rstrip():
            self.StatusListbox.config(state=NORMAL)
            self.StatusListbox.delete(x,x)
            self.StatusListbox.insert(x, "SAVED")
            self.StatusListbox.itemconfig(x, bg="green", fg="white")
            found = True
         x += 1