from PyQt4 import QtGui, QtCore
from Deque_Widget_Class import *
import time, threading, os, sys
from Queue_Class import Queue_Class 
#import sound_interface
#from Db_Class import Db_Class

#dbm = Db_Class()

class ReleaserGUI2(QtGui.QWidget):
   def __init__(self):
      QtGui.QWidget.__init__(self)
      #self.deque = Queue_Class()
      self.initUI()          
 
        
   def initUI(self):
      entireHbox      = QtGui.QHBoxLayout()
      
      queueHbox       = QtGui.QHBoxLayout()
      interfaceVBox   = QtGui.QVBoxLayout()
      interfaceHBox   = QtGui.QVBoxLayout()
      
      Row0HBox = QtGui.QHBoxLayout()
      Row1HBox = QtGui.QHBoxLayout()
      Row2HBox = QtGui.QHBoxLayout()

      ### Deque
      self.dequeWidget = DequeWidget()
      self.dequeWidget.setFixedWidth(175)
      queueHbox.addWidget(self.dequeWidget)

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

      Row1HBox.addWidget(self.releaseButton)
      interfaceVBox.addLayout(Row1HBox)
      
      '''Assemble Window'''
      entireHbox.addLayout(queueHbox)
      entireHbox.addLayout(interfaceVBox)
      self.setLayout(entireHbox)
      self.setGeometry(100, 100, 300, 400)
      self.setWindowTitle('Releasing App')
      self.show()


   def ManualReleaseClicked(self):
      try:
         self.deque.removeFromTopOfQueue()
         ubit = self.dequeWidget.pop().text()
      except KeyError:
         return
      #sound_interface.play_wav_file(wavpath)
      os.system('aplay ../../res/namewavs/%s.wav' % ubit)