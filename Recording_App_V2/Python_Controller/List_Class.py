from PyQt4 import QtGui, QtCore
from utils import *


class ListWidget(QtGui.QListWidget):
    def __init__(self):
        QtGui.QListWidget.__init__(self)

    def addToList(self, name):   
        ubit = QtGui.QListWidgetItem(name)
        if check_file_exists(str(name) + ".wav"):
            ubit.setIcon(QtGui.QIcon(r"Pictures\check.png"))
        else:
            ubit.setIcon(QtGui.QIcon(r"Pictures\x.png"))
        ubit.setFont(QtGui.QFont('Verdana', weight=4))
        self.addItem(ubit)
        self.sortItems(0)
        
    def findName(self, name):
        try:
            return self.findItems(name, QtCore.Qt.MatchExactly)[0] 
        except IndexError:
            return False