from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal
from Deque_Widget_Class import *
import time, threading


class ReleaserGUI(QtGui.QWidget):
   def __init__(self):
      QtGui.QWidget.__init__(self)
      self.TIME_RUNNING = False
      self.CURRENT_TIME = "0.0"
      self.RELEASE_TIME = "2.5"
      self.TIME_PAUSED = False
      self.CONNECTED = False
      
      self.initUI()       
      self.initConnection()
      # connect slots
      self.connectSlots()
      self.initClock()
    
   def initConnection(self):
      self.ConnectionTrigger = ConnTrigger()
      self.Connectionthread = threading.Thread(target=self.connection_updater)
      self.Connectionthread.daemon = True
      self.Connectionthread.start()
      
       ####################################
    #   Thread to Update Progress Bar
    ####################################
   def connection_updater(self):
      while(1):
         if self.CONNECTED == True:
            self.ConnectionTrigger.trigger.connect(self.receiveConnTrigger)
            self.ConnectionTrigger.trigger.emit(1)
            time.sleep(0.1) 
         else:
            self.ConnectionTrigger.trigger.connect(self.receiveConnTrigger)
            self.ConnectionTrigger.trigger.emit(0)
            time.sleep(0.1)
         time.sleep(1)
   
   @QtCore.pyqtSlot(int)
   def receiveConnTrigger(self,num):
      if num == 1:
         self.connectionIcon.setPixmap(QtGui.QPixmap("Pictures/green_dot.png"))
      else:
         self.connectionIcon.setPixmap(QtGui.QPixmap("Pictures/red_dot.png"))
        #self.connectionIcon.setText(str(num))

        
   def initUI(self):
      ######################################################
      #  _______    ___________            _____________   #
      # | queue |->|__release__|    or    |__use timer__|  #
      # |       |   _____   _____   _____   _____   _____  #
      # |       |  |_img_| |_bar_| |_img_| |_ply_| |_hld_| #
      # |       |   __________              _____________  #
      # |_______|<-|_incoming_|            |__time__|_sec| #
      #                                                    #
      ######################################################
      entireHbox      = QtGui.QHBoxLayout()
      
      queueHbox       = QtGui.QHBoxLayout()
      interfaceVBox   = QtGui.QVBoxLayout()
      interfaceHBox   = QtGui.QVBoxLayout()
      
      Row0HBox = QtGui.QHBoxLayout()
      Row1HBox = QtGui.QHBoxLayout()
      Row2HBox = QtGui.QHBoxLayout()
      Row3HBox = QtGui.QHBoxLayout()
      Row4HBox = QtGui.QHBoxLayout()

      TimerTime1HBox = QtGui.QHBoxLayout()
      TimerTime2HBox = QtGui.QHBoxLayout()
      TimerV1Box = QtGui.QVBoxLayout()
      TimerV2Box = QtGui.QVBoxLayout()
      TimerButtonVBox = QtGui.QVBoxLayout() 
      TimerHBox = QtGui.QHBoxLayout()
      TimerH1Box = QtGui.QHBoxLayout()
      TimerVBox = QtGui.QVBoxLayout()
      SpacerBox1 = QtGui.QVBoxLayout()
      
      ### Deque
      self.dequeWidget = DequeWidget()
      self.dequeWidget.setFixedWidth(175)
      queueHbox.addWidget(self.dequeWidget)
      

      
      ### Outgoing Arrow Icon
      self.arrowIcon = QtGui.QLabel()
      self.arrowIcon.setPixmap(QtGui.QPixmap("Pictures/right_arrow.gif"))
      self.arrowIcon.setFixedHeight(30)
      self.arrowIcon.setFixedWidth(60)
      self.arrowIcon.setAlignment(QtCore.Qt.AlignCenter)
      ### Incoming Arrow Icon
      self.arrowIcon = QtGui.QLabel()
      self.arrowIcon.setPixmap(QtGui.QPixmap("Pictures/left_arrow.gif"))
      self.arrowIcon.setFixedHeight(30)
      self.arrowIcon.setFixedWidth(60)
      self.arrowIcon.setAlignment(QtCore.Qt.AlignCenter)

      
      
      '''ROW 1'''
      mainfont = QtGui.QFont("Verdana", 14, QtGui.QFont.Bold)
      ### Release Button
      self.releaseButton = QtGui.QPushButton()
      self.releaseButton.setText("MANUAL\nRELEASE")
      self.releaseButton.setFont(mainfont)
      self.releaseButton.clicked.connect(self.ManualReleaseClicked)
      self.releaseButton.setFixedWidth(180)
      self.releaseButton.setStyleSheet("QPushButton         {color: rgb(177,177,255);background: rgb(38,38,255) }"
                                       "QPushButton:pressed {color: rgb(38,38,255);background: rgb(177,177,255) }" )  
      ### OR Label
      self.orLabel = QtGui.QLabel(" OR ")
      self.orLabel.setStyleSheet("background: rgb(177,177,255); border: 1px solid;")
      qf = QtGui.QFont("Verdana", 10)#, QtGui.QFont.Bold)
      self.orLabel.setFont(qf)
      self.orLabel.setFixedHeight(30)
      self.orLabel.setFixedWidth(40)
      self.orLabel.setAlignment(QtCore.Qt.AlignCenter)

      ### Use Timer Button
      self.useTimerButton = QtGui.QPushButton()
      self.useTimerButton.setText("AUTOMATIC\nTIMER")
      self.useTimerButton.setFont(mainfont)
      self.useTimerButton.clicked.connect(self.AutomaticReleaseClicked)
      #self.useTimerButton.setIcon(QtGui.QIcon(r"Pictures/record_button.gif"))
      self.useTimerButton.setFixedWidth(245)
      self.useTimerButton.setStyleSheet("QPushButton         {color: rgb(177,177,255);background: rgb(38,38,255) }"
                                        "QPushButton:pressed {color: rgb(38,38,255);background: rgb(177,177,255) }" )

      
      
      
      self.manualSelected = QtGui.QLabel("Manual Mode Selected")
      self.manualSelected.setStyleSheet("color: red;")
      qf = QtGui.QFont("Verdana", 8)#, QtGui.QFont.Bold)
      self.manualSelected.setFont(qf)
      self.manualSelected.setFixedHeight(20)
      self.manualSelected.setFixedWidth(180)
      self.manualSelected.setAlignment(QtCore.Qt.AlignCenter)
      
      self.spacer = QtGui.QLabel("   ")
      qf = QtGui.QFont("Verdana", 8)#, QtGui.QFont.Bold)
      self.spacer.setFont(qf)
      self.spacer.setFixedHeight(20)
      self.spacer.setFixedWidth(40)
      self.spacer.setAlignment(QtCore.Qt.AlignCenter)
      
      self.autoSelected = QtGui.QLabel()
      self.autoSelected.setStyleSheet("color: red;")
      qf = QtGui.QFont("Verdana", 8)#, QtGui.QFont.Bold)
      self.autoSelected.setFont(qf)
      self.autoSelected.setFixedHeight(20)
      self.autoSelected.setFixedWidth(245)
      self.autoSelected.setAlignment(QtCore.Qt.AlignCenter)
      
      
      Row0HBox.addWidget(self.manualSelected)
      Row0HBox.addWidget(self.spacer)
      Row0HBox.addWidget(self.autoSelected)
      interfaceVBox.addLayout(Row0HBox)
      
      Row1HBox.addWidget(self.releaseButton)
      Row1HBox.addWidget(self.orLabel)
      Row1HBox.addWidget(self.useTimerButton)
      interfaceVBox.addLayout(Row1HBox)
      
      
      '''ROW 2'''
      ### Current Time
      timerfont = QtGui.QFont("Verdana", 18, QtGui.QFont.Bold)
      
      self.TimeLabel = QtGui.QLabel("Time")
      self.TimeLabel.setStyleSheet("color: rgb(177,177,255); background: rgb(38,38,255); border: 1px solid;")
      qf = QtGui.QFont("Verdana", 14)
      self.TimeLabel.setFont(qf)
      self.TimeLabel.setFixedHeight(30)
      self.TimeLabel.setFixedWidth(245)
      self.TimeLabel.setAlignment(QtCore.Qt.AlignCenter)
      
      self.currentTimeLabel = QtGui.QLabel("Current")
      self.currentTimeLabel.setStyleSheet("background: rgb(177,177,255); border: 3px solid;")
      qf = QtGui.QFont("Verdana", 10)
      self.currentTimeLabel.setFont(qf)
      self.currentTimeLabel.setFixedHeight(30)
      self.currentTimeLabel.setFixedWidth(95)
      self.currentTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
      
      self.releaseTimeLabel = QtGui.QLabel(" Send @")
      self.releaseTimeLabel.setStyleSheet("background: rgb(177,177,255); border: 3px solid;")
      qf = QtGui.QFont("Verdana", 10)
      self.releaseTimeLabel.setFont(qf)
      self.releaseTimeLabel.setFixedHeight(30)
      self.releaseTimeLabel.setFixedWidth(95)
      self.releaseTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
      
      # Current Time
      self.Current = QtGui.QLabel("0.0")
      self.Current.setFixedWidth(65)
      self.Current.setStyleSheet("color: rgb(27,0,115)")
      self.Current.setFont(timerfont)
      self.Current.setAlignment(QtCore.Qt.AlignCenter)

      # Release Time
      self.Release = QtGui.QLabel("2.5")
      self.Release.setFixedWidth(65)
      self.Release.setStyleSheet("color: rgb(27,0,115)")
      self.Release.setFont(timerfont)
      self.Release.setAlignment(QtCore.Qt.AlignCenter)

      ### Up Button
      self.upButton = QtGui.QPushButton()
      self.upButton.clicked.connect(self.upClicked)
      self.upButton.setIcon(QtGui.QIcon(r"Pictures/up.png"))
      self.upButton.setFixedWidth(40)
      
      ### Down Button
      self.downButton = QtGui.QPushButton()
      self.downButton.clicked.connect(self.downClicked)
      self.downButton.setIcon(QtGui.QIcon(r"Pictures/down.png"))
      self.downButton.setFixedWidth(40)
      
      buttonfont = QtGui.QFont("Verdana", 10, QtGui.QFont.Bold)
      ### Stop Button
      self.stopButton = QtGui.QPushButton("STOP")
      self.stopButton.clicked.connect(self.stopButtonClicked)
      self.stopButton.setFixedWidth(117)
      self.stopButton.setStyleSheet("color: rgb(177,177,255); background: red")
      self.stopButton.setFont(buttonfont)
      
      ### Start Button
      self.startButton = QtGui.QPushButton("START")
      self.startButton.clicked.connect(self.startButtonClicked)
      self.startButton.setFixedWidth(118)
      self.startButton.setStyleSheet("color: rgb(177,177,255); background: green")
      self.startButton.setFont(buttonfont)
         
      
      TimerButtonVBox.addWidget(self.upButton)
      TimerButtonVBox.addWidget(self.downButton)
      
      TimerTime1HBox.addWidget(self.Current) 
      TimerTime2HBox.addWidget(self.Release)       
      
      TimerH1Box.addWidget(self.startButton)
      TimerH1Box.addWidget(self.stopButton) 
      
      TimerV1Box.addWidget(self.currentTimeLabel)
      TimerV2Box.addWidget(self.releaseTimeLabel)
      TimerV1Box.addLayout(TimerTime1HBox)
      TimerV2Box.addLayout(TimerTime2HBox)

      
      self.SpaceLabel = QtGui.QLabel("  ")
      self.SpaceLabel.setFixedWidth(230)
      SpacerBox1.addWidget(self.SpaceLabel)
      
      TimerHBox.addLayout(TimerV1Box)
      TimerHBox.addLayout(TimerV2Box)
      TimerHBox.addLayout(TimerButtonVBox)
      TimerVBox.addLayout(TimerHBox)
      TimerVBox.addWidget(self.TimeLabel)
      TimerVBox.addLayout(TimerH1Box)
      
      Row2HBox.addLayout(SpacerBox1)
      Row2HBox.addLayout(TimerVBox)
      interfaceVBox.addLayout(Row2HBox)
      
      
      '''ROW 3'''
      ### Podium Icon
      self.podiumIcon = QtGui.QLabel()
      self.podiumIcon.setPixmap(QtGui.QPixmap("Pictures/podium.png"))
      self.podiumIcon.setFixedHeight(80)
      self.podiumIcon.setFixedWidth(40)
      self.podiumIcon.setAlignment(QtCore.Qt.AlignCenter)
      
      arrowfont = QtGui.QFont("Verdana", 8, QtGui.QFont.Bold)
      ### Footstep Icons
      self.footstep1 = QtGui.QLabel(">>")
      self.footstep1.setFixedHeight(20)
      self.footstep1.setFixedWidth(20)
      self.footstep1.setFont(arrowfont)
      self.footstep1.setAlignment(QtCore.Qt.AlignCenter)
      #
      self.footstep2 = QtGui.QLabel(">>")
      self.footstep2.setFixedHeight(20)
      self.footstep2.setFixedWidth(20)
      self.footstep2.setFont(arrowfont)
      self.footstep2.setAlignment(QtCore.Qt.AlignCenter)
      #
      self.footstep3 = QtGui.QLabel(">>")
      self.footstep3.setFixedHeight(20)
      self.footstep3.setFixedWidth(20)
      self.footstep3.setFont(arrowfont)
      self.footstep3.setAlignment(QtCore.Qt.AlignCenter)
      #
      self.footstep4 = QtGui.QLabel(">>")
      self.footstep4.setFixedHeight(20)
      self.footstep4.setFixedWidth(20)
      self.footstep4.setFont(arrowfont)
      self.footstep4.setAlignment(QtCore.Qt.AlignCenter)
      #      
      self.footstep5 = QtGui.QLabel(">>")
      self.footstep5.setFixedHeight(20)
      self.footstep5.setFixedWidth(20)
      self.footstep5.setFont(arrowfont)
      self.footstep5.setAlignment(QtCore.Qt.AlignCenter)
      #
      self.footstep6 = QtGui.QLabel(">>")
      self.footstep6.setFixedHeight(20)
      self.footstep6.setFixedWidth(20)
      self.footstep6.setFont(arrowfont)
      self.footstep6.setAlignment(QtCore.Qt.AlignCenter)
      #      
      self.footstep7 = QtGui.QLabel(">>")
      self.footstep7.setFixedHeight(20)
      self.footstep7.setFixedWidth(20)
      self.footstep7.setFont(arrowfont)
      self.footstep7.setAlignment(QtCore.Qt.AlignCenter)
      #      
      self.footstep8 = QtGui.QLabel(">>")
      self.footstep8.setFixedHeight(20)
      self.footstep8.setFixedWidth(20)
      self.footstep8.setFont(arrowfont)
      self.footstep8.setAlignment(QtCore.Qt.AlignCenter)
      #      
      self.footstep9 = QtGui.QLabel(">>")
      self.footstep9.setFixedHeight(20)
      self.footstep9.setFixedWidth(20)
      self.footstep9.setFont(arrowfont)
      self.footstep9.setAlignment(QtCore.Qt.AlignCenter)
      #      
      self.footstep10 = QtGui.QLabel(">>")
      self.footstep10.setFixedHeight(20)
      self.footstep10.setFixedWidth(20)
      self.footstep10.setFont(arrowfont)
      self.footstep10.setAlignment(QtCore.Qt.AlignCenter)
      
      ### Handshake Icon      
      self.handshake = QtGui.QLabel()
      self.handshake.setPixmap(QtGui.QPixmap("Pictures/handshake.png"))
      self.handshake.setFixedHeight(40)
      self.handshake.setFixedWidth(60)
      self.handshake.setAlignment(QtCore.Qt.AlignCenter)
      
      Row3HBox.addWidget(self.podiumIcon)
      Row3HBox.addWidget(self.footstep1)
      Row3HBox.addWidget(self.footstep2)
      Row3HBox.addWidget(self.footstep3)
      Row3HBox.addWidget(self.footstep4)
      Row3HBox.addWidget(self.footstep5)
      Row3HBox.addWidget(self.footstep6)
      Row3HBox.addWidget(self.footstep7)
      Row3HBox.addWidget(self.footstep8)
      Row3HBox.addWidget(self.footstep9)
      Row3HBox.addWidget(self.footstep10)
      Row3HBox.addWidget(self.handshake)
      interfaceVBox.addLayout(Row3HBox)
      
      
      '''ROW 4'''
      self.connectionIcon = QtGui.QLabel("Connection Status: ")
      self.connectionIcon.setFixedHeight(25)
      qf = QtGui.QFont("Verdana", 12)
      self.connectionIcon.setFont(qf)
      #self.connectionIcon.setFixedWidth(25)
      self.connectionIcon.setAlignment(QtCore.Qt.AlignRight)
      Row4HBox.addWidget(self.connectionIcon)
      
      ### connection Icon      
      self.connectionIcon = QtGui.QLabel()
      self.connectionIcon.setFixedHeight(25)
      self.connectionIcon.setFixedWidth(25)
      self.connectionIcon.setAlignment(QtCore.Qt.AlignCenter)
      Row4HBox.addWidget(self.connectionIcon)
      interfaceVBox.addLayout(Row4HBox)

      '''Assemble Window'''
      entireHbox.addLayout(queueHbox)
      entireHbox.addLayout(interfaceVBox)
      self.setLayout(entireHbox) 
      self.setGeometry(100, 100, 700, 400)
      self.setWindowTitle('Releasing App')   
      self.show()
   
   def initClock(self):
      self.clockThread = threading.Thread(target=self.clockTimer)
      self.clockThread.daemon = True
      self.clockThread.start()
   
   
   def runFootsteps(self):
      self.FeetThread = threading.Thread(target=self.walkFeet)
      self.FeetThread.daemon = True
      self.FeetThread.start()
    
   def walkFeet(self):
      pass
      # self.footstep1.setText("  ")
      # time.sleep(0.2)
      # self.footstep1.setText(">>")
      # self.footstep2.setText("  ")
      # time.sleep(0.2)
      # self.footstep2.setText(">>")
      # self.footstep3.setText("  ")
      # time.sleep(0.2)
      # self.footstep3.setText(">>")
      # self.footstep4.setText("  ")
      # time.sleep(0.2)
      # self.footstep4.setText(">>")
      # self.footstep5.setText("  ")
      # time.sleep(0.2)
      # self.footstep5.setText(">>")
      # self.footstep6.setText("  ")
      # time.sleep(0.2)
      # self.footstep6.setText(">>")
      # self.footstep7.setText("  ")
      # time.sleep(0.2)
      # self.footstep7.setText(">>")
      # self.footstep8.setText("  ")
      # time.sleep(0.2)
      # self.footstep8.setText(">>")
      # self.footstep9.setText("  ")
      # time.sleep(0.2)
      # self.footstep9.setText(">>")
      # self.footstep10.setText("  ")
      # time.sleep(0.2)
      # self.footstep10.setText(">>")

     
     
   def clockTimer(self):
      self.onesCount = 0
      self.onesCountLock= threading.Lock()
      self.tenthsCount = 0
      self.tenthsCountLock= threading.Lock()
      while(1):
         self.tenthsCountLock.acquire()
         self.onesCountLock.acquire()
         if(self.TIME_RUNNING == True):
            self.tenthsCount += 1
            if self.tenthsCount == 10:
               self.tenthsCount = 0
               self.onesCount += 1
               if self.onesCount == 10:
                  self.onesCount = 0   
         self.CURRENT_TIME = str(self.onesCount)+"."+str(self.tenthsCount)
         self.Current.setText(str(self.onesCount)+"."+str(self.tenthsCount))
         self.tenthsCountLock.release()
         self.onesCountLock.release()
         time.sleep(0.1)
   
   
   def ManualReleaseClicked(self):
      self.dequeWidget.pop()
      self.onesCountLock.acquire()
      self.tenthsCountLock.acquire()
      trackOnes = self.onesCount
      trackTenths = self.tenthsCount
      self.onesCount = 0
      self.tenthsCount = 0
      self.tenthsCountLock.release()
      self.onesCountLock.release()
      print str(trackOnes) + "." + str(trackTenths)
      self.runFootsteps()
      self.manualSelected.setText("Manual Mode Selected")
      self.autoSelected.setText("                      ")
      #self.dequeTrigger = DequeTrigger()
   
   def AutomaticReleaseClicked(self):
      self.automaticThread = threading.Thread(target=self.AutomaticRelease)
      self.automaticThread.daemon = True
      self.automaticThread.start()
      self.manualSelected.setText("                    ")
      self.autoSelected.setText("Automatic Mode Selected")

   
   def AutomaticRelease(self):
      self.CURRENT_TIME_LOCK= threading.Lock()
      while(1):
         time.sleep(0.1)
         self.CURRENT_TIME_LOCK.acquire()
         if self.CURRENT_TIME == self.RELEASE_TIME:
            self.onesCount = 0
            self.tenthsCount = 0
            self.dequeWidget.pop()
         self.CURRENT_TIME_LOCK.release()
   
   def upClicked(self):
      self.RELEASE_TIME_LOCK = threading.Lock()
      self.RELEASE_TIME_LOCK.acquire()
      time = self.RELEASE_TIME.split(".")
      ones = int(time[0])
      tens = int(time[1])
      if tens == 9:
         tens = 0
         ones += 1
         if ones == 9:
            ones = 0
      else:
         tens += 1
      time = str(ones)+"."+str(tens)
      self.RELEASE_TIME = str(ones)+"."+str(tens)
      self.Release.setText(time)
      self.RELEASE_TIME_LOCK.release()
         
      
   def downClicked(self):
      self.RELEASE_TIME_LOCK = threading.Lock()
      self.RELEASE_TIME_LOCK.acquire()
      time = self.RELEASE_TIME.split(".")
      ones = int(time[0])
      tens = int(time[1])
      if tens == 0 and ones == 0:
         pass
      elif tens == 0:
         tens = 9
         ones -= 1
         if ones == 0 or ones == -1:
            ones = 0
      else:
         tens -= 1
      time = str(ones)+"."+str(tens)
      self.RELEASE_TIME = str(ones)+"."+str(tens)
      self.Release.setText(time)
      self.RELEASE_TIME_LOCK.release()
   
   
   def stopButtonClicked(self):
      self.STOP_TIME_LOCK = threading.Lock()
      self.STOP_TIME_LOCK.acquire()
      self.TIME_RUNNING = False
      self.onesCount = 0
      self.tenthsCount = 0
      self.CURRENT_TIME = "0.0"
      self.STOP_TIME_LOCK.release()
   
   def startButtonClicked(self):
      self.START_TIME_LOCK = threading.Lock()
      self.START_TIME_LOCK.acquire()
      self.TIME_RUNNING = True
      self.onesCount = 0
      self.tenthsCount = 0
      self.CURRENT_TIME = "0.0"
      self.START_TIME_LOCK.release()
      
     
   def connectSlots(self):
      pass

class DequeTrigger(QtCore.QObject):
   trigger = QtCore.pyqtSignal(str)

class ConnTrigger(QtCore.QObject):
    trigger = QtCore.pyqtSignal(int)