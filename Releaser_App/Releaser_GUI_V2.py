from PyQt4 import QtGui, QtCore
from Deque_Widget_Class import *
import time, threading


class ReleaserGUI2(QtGui.QWidget):
   def __init__(self):
      QtGui.QWidget.__init__(self)
      self.initUI()       

    
   def initConnection(self):
      self.ConnectionTrigger = ConnTrigger()
      self.Connectionthread = threading.Thread(target=self.connection_updater)
      self.Connectionthread.daemon = True
      self.Connectionthread.start()
      
        
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
      self.dequeWidget.pop()
