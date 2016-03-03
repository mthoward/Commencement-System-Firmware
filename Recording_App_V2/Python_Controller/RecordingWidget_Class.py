from PyQt4 import QtGui, QtCore
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from PlotFigure_Class import *
from List_Class import *
from MicRecorder_Class import *
from sound_interface import *

class RecordingWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.recordingBool = 0
        # customize the UI
        self.initUI()
        
        # init class data
        self.initMic()       
        
        # connect slots
        self.connectSlots()
        
        # init MPL widget
        self.initMplWidget()
        

    def initUI(self):
        ##########################################
        #  _______    _____________              #
        # | list  |  |__show_name__|             #
        # |       |   _____   _________   _____  #
        # |       |  |_rec_| |___bar___| |_ply_| #
        # |       |   _________________________  #
        # |       |  |        waveform         | #
        # |_______|  |_________________________| #
        #                                        #
        ##########################################
        displayVbox = QtGui.QVBoxLayout()
        
        ### Show Name
        self.showName = QtGui.QLabel("Select From List")
        self.showName.setStyleSheet("background: white; border: 1px solid;")
        qf = QtGui.QFont("Verdana", 10)#, QtGui.QFont.Bold)
        self.showName.setFont(qf)
        self.showName.setAlignment(QtCore.Qt.AlignCenter)

        
        ### Buttons
        buttonBox = QtGui.QHBoxLayout()
        self.buttonRec = QtGui.QPushButton()
        self.buttonRec.setText("REC")
        self.buttonRec.clicked.connect(self.beginRec)
        self.buttonRec.setIcon(QtGui.QIcon(r"Pictures\record_button.gif"))
        self.buttonRec.setFixedWidth(70)
        self.buttonRec.setStyleSheet("background: rgb(250,102,102)")
        self.buttonPlay = QtGui.QPushButton()
        self.buttonPlay.setText("PLAY")
        self.buttonPlay.setIcon(QtGui.QIcon(r"Pictures\play_button.gif"))
        self.buttonPlay.setFixedWidth(70)
        self.buttonPlay.setStyleSheet("background: rgb(92,214,92)")
        self.buttonPlay.clicked.connect(self.playback)
        buttonBox.addWidget(self.showName)
        buttonBox.addWidget(self.buttonRec)
        buttonBox.addWidget(self.buttonPlay)
        ### Add Name and Buttons to Layout
        #displayVbox.addLayout(showNameBox)
        displayVbox.addLayout(buttonBox)
        
        ### Progress Bar
        barBox = QtGui.QHBoxLayout()
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setRange(0, 30)
        self.progressBar.setValue(0)
        barBox.addWidget(self.progressBar)
        displayVbox.addLayout(barBox)
        self.progressBar.show()
        
        ### PLOT
        self.main_figure = PlotFigure(self)
        displayVbox.addWidget(self.main_figure.canvas)
        
        ### LIST
        listbox = QtGui.QVBoxLayout()
        self.font = QtGui.QFont("Verdana", 12, QtGui.QFont.Bold)
        self.listLabel = QtGui.QLabel('UBIT Names')
        self.listLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.listLabel.setFont(self.font)

        self.listLabel.setStyleSheet("background-color: rgb(2,176,250); color: white")
        self.list = ListWidget()
        self.list.itemClicked.connect(self.changeLabel)
        self.list.setFixedWidth(175)
        self.list.setStyleSheet("")
        
        ### List Helpers
        self.searchButton = QtGui.QLabel()
        self.searchButton.setPixmap(QtGui.QPixmap("mag_glass.png"))
        QtCore.QObject.connect(self.searchButton, QtCore.SIGNAL('clicked()'), self.searchClicked)
        self.searchButton.mousePressEvent = self.searchClicked
        self.searchButton.setFixedWidth(40)
        self.searchButton.setFixedHeight(40)
        self.searchName = QtGui.QLineEdit()
        self.searchName.setFixedWidth(130)
        
        self.searchBox = QtGui.QHBoxLayout()
        self.searchBox.addWidget(self.searchName)
        self.searchBox.addWidget(self.searchButton)
        listbox.addWidget(self.listLabel)
        listbox.addWidget(self.list)
        listbox.addLayout(self.searchBox)
        
        ### Total Window
        FrameBox = QtGui.QHBoxLayout()
        FrameBox.addLayout(listbox)
        FrameBox.addLayout(displayVbox)
        
        self.setLayout(FrameBox) 
        self.setGeometry(100, 100, 550, 300)
        self.setWindowTitle('Recording App')   
        self.show()
        
        ### Refreshs Graph Data
        timer = QtCore.QTimer()
        timer.timeout.connect(self.handleNewData)
        timer.start(50)
        # keep reference to timer        
        self.timer = timer
    
     
    ####################################
    #   Record WAV File &
    #   Control Timing
    ####################################     
    def beginRec(self):
        self.showName.setStyleSheet("background: white; border: 1px solid; color: black")
        if ((self.list.currentItem() is None) or (self.showName.text() == "Select From List")):
            self.showName.setStyleSheet("color: red")
            self.showName.setText("No Name Selected")
        else:      
            self.progBarTrigger = ProgressBarTrigger()
            self.holdTrigger = TimerTrigger()
            self.recordingBool = 1
            self.thread2 = threading.Thread(target=self.progress_bar_updater)
            self.thread2.start()
            self.thread3 = threading.Thread(target=self.record_wav_file_wrapper)
            self.thread3.start()
            self.thread4 = threading.Thread(target=self.holdingTimer)
            self.thread4.start()
    
    def record_wav_file_wrapper(self):
        record_wav_file(self.showName.text())

        
    ####################################
    #   Play WAV File &
    #   Control Timing
    ####################################        
    def playback(self):
        self.playThread = threading.Thread(target=self.play_wav_file_wrapper)
        self.playThread.start() 
    
    def play_wav_file_wrapper(self):
        play_wav_file(self.showName.text())


    ####################################
    #   Thread to Update Progress Bar
    ####################################
    def progress_bar_updater(self):
        for x in range(0,31):
            self.progBarTrigger.trigger.connect(self.receiverTrigger)
            self.progBarTrigger.trigger.emit(x)
            time.sleep(0.07) 
        self.progBarTrigger.trigger.connect(self.receiverTrigger)
        self.progBarTrigger.trigger.emit(0)    
    @QtCore.Slot(int)
    def receiverTrigger(self,num):
        self.progressBar.setValue(num)
    
    
    ####################################
    #   Thread to Control Sleep Timers
    ####################################
    def holdingTimer(self):
        time.sleep(3)
        self.holdTrigger.trigger.connect(self.timerTrigger)
        self.holdTrigger.trigger.emit(0)
    
    @QtCore.Slot(int)
    def timerTrigger(self,num):    
        self.recordingBool = num
        self.list.currentItem().setIcon(QtGui.QIcon(r"Pictures\check.png"))
    
    
    
    ####################################
    #   Initialize Mic Object
    ####################################
    def initMic(self):
        self.mic = MicRecorder()
        self.mic.start()  
        self.time_vect = np.arange(0,self.mic.chunksize, dtype=np.float32) / self.mic.rate * 1000     
      
    def connectSlots(self):
        pass
    
    
    ####################################
    #   Creates Matplotlib Plot
    ####################################
    def initMplWidget(self):
        # top plot
        self.ax_top = self.main_figure.figure.add_subplot(111)
        self.ax_top.set_ylim(-1000, 1000)
        self.ax_top.set_xlim(0, self.time_vect.max())
        self.line_top, = self.ax_top.plot(self.time_vect, 
                                         np.ones_like(self.time_vect))                      
        self.main_figure.figure.subplots_adjust(left=0.0, top=1.0, bottom=0.0, right=1.0)
    
    
    ####################################
    #   Gets Data for Plot & Draws It
    ####################################
    def handleNewData(self):        
        # gets the latest frames        
        frames = self.mic.get_frames()
        
        if len(frames) > 0:
            # keeps only the last frame
            current_frame = frames[-1]
            # plots the time signal
            self.line_top.set_data(self.time_vect, current_frame)
            if self.recordingBool == 1:
               self.main_figure.canvas.draw()
    
    
    ####################################
    #   Change UBIT Name Label
    ####################################
    def changeLabel(self, item):
        self.showName.setText(item.text())
 
 
    ####################################
    #   Search List Button
    ####################################
    @QtCore.Slot()
    def searchClicked(self, event):
        result = self.list.findName(self.searchName.text())
        if result != False:
            self.list.setCurrentItem(result)
            self.searchName.setStyleSheet("color: black;")
            self.showName.setText(self.list.currentItem().text())
        else:
            self.searchName.setStyleSheet("color: red;")
            self.searchName.setText("Not Found")

            
####################################
#   Trigger Classes
####################################
class ProgressBarTrigger(QtCore.QObject):
    trigger = QtCore.Signal(int)

class TimerTrigger(QtCore.QObject):
    trigger = QtCore.Signal(int)    

