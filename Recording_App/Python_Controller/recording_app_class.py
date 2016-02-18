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
      ### Set Grid Layout, Non-resizable
      self.grid()
      self.resizable(False,False)

      ### Set Col Weights
      for x in range(0,5):
         if x == 1:
            self.columnconfigure(x,weight=1, minsize=80)
         if x == 2:
            self.columnconfigure(x,weight=0)
         else:
            self.columnconfigure(x,weight=1)

      ### Set Row Weights
      for x in range(0,6):
         self.rowconfigure(x,weight=1)

      ### Set "Width x Height"
      self.geometry('400x200')


      ### UBIT Listbox
      self.UBITListbox = Listbox(self)
      self.UBITListbox.grid(row=1, column=1,
                        rowspan=6,
                        columnspan=1,
                        padx=8,
                        pady=8,
                        sticky='NSEW')
      self.UBITListbox.columnconfigure(0,weight=1)
      for x in range(0,5):
         self.UBITListbox.rowconfigure(x,weight=1)
      
      ### Status Listbox
      self.StatusListbox = Listbox(self)
      self.StatusListbox.grid(row=1,
                              column=0,
                              rowspan=9,
                              pady=8,
                              sticky='NSEW')
      self.StatusListbox.columnconfigure(0,weight=1)
      for x in range(0,5):
         self.StatusListbox.rowconfigure(x,weight=1)
         
         

      ### Scrollbar
      self.scrollbar = Scrollbar(self.UBITListbox,
                                 orient=VERTICAL,
                                 command=self.OnVsb)
      self.UBITListbox.config(yscrollcommand=self.scrollbar.set,
                              activestyle=NONE)
      self.StatusListbox.config(yscrollcommand=self.scrollbar.set,
                                width=5,
                                exportselection=0,
                                activestyle=NONE)
      self.scrollbar.grid(column=1, rowspan=6, sticky='NS')
      self.selection = self.UBITListbox.get(ACTIVE)

      
      ### '>>>' button
      self.listButtonVariable = Tkinter.StringVar()
      self.listButtonVariable.set(">>>")
      selButton = Tkinter.Button(self,
                                 textvariable=self.listButtonVariable,
                                 command=self.GetSelection)
      selButton.grid(column=2, row=1, rowspan=3, padx=8)

      
      ### Label Over Test Entry
      self.label = Label(self, text="Selected UBIT")
      self.label.grid(column=3, row=1, columnspan=2,padx=8)

      ### Text Entry
      self.entryString = StringVar()
      self.entry = Tkinter.Entry(self, textvariable=self.entryString)
      #self.entry.config(width=15)
      self.entry.grid(column=3,
                      row=2,
                      padx=8,
                      columnspan=2,
                      sticky='EW')
      self.entryString.set("")


      ### Record Button
      self.rec_image = Tkinter.PhotoImage(file="record_button.gif")
      self.buttonVariable = Tkinter.StringVar()
      self.buttonVariable.set(" Record ")
      self.button = Tkinter.Button(self,
                              textvariable=self.buttonVariable,
                              command=self.RecordPressed,
                              bg="gray",
                              fg="red")

      self.button.config(image=self.rec_image)
      self.button.grid(column=3, row=4)

      ### Playback button
      self.play_image = Tkinter.PhotoImage(file="play_button.gif")
      self.playbackVariable = Tkinter.StringVar()
      self.playbackVariable.set("Playback")
      self.playbutton = Tkinter.Button(self,
                              textvariable=self.playbackVariable,
                              command=self.PlaybackPressed,
                              bg="gray",
                              fg="blue")
      self.playbutton.config(image=self.play_image)
      self.playbutton.grid(column=4, row=4)

      # Add Labels Under Buttons
      self.statusLabel = Label(self, text='', fg="red")
      self.statusLabel.grid(column=3, row=6,
                            columnspan=2,padx=8)
                             
      self.recordLabel = Label(self, text='Record', fg="red")
      self.recordLabel.grid(column=3, row=3,padx=8)
      
      self.playLabel = Label(self, text=' Play ', fg="blue")
      self.playLabel.grid(column=4, row=3,padx=8)
      
      
      # Add Progressbar
      self.add_progress_bar(30,145,col=3,row=5)
      
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
      # Playback
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
   
   def add_progress_bar(self, max, length, col, row):
      self.barStyle = ttk.Style()
      self.barStyle.theme_use('clam')
      self.barStyle.configure("red.Horizontal.TProgressbar", foreground="red", background="red")
      self.barVariable = Tkinter.IntVar()
      self.bar = ttk.Progressbar(self,
                                 orient=HORIZONTAL,
                                 length=length,
                                 mode='determinate',
                                 maximum=max,
                                 variable = self.barVariable,
                                 style="red.Horizontal.TProgressbar")
      self.bar.grid(column=col, row=row, columnspan=2,pady=8)
