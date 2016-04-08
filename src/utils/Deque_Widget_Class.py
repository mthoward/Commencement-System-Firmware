from PyQt4 import QtGui

class DequeWidget(QtGui.QListWidget):
    def __init__(self):
        QtGui.QListWidget.__init__(self)

    def addToQueue(self, name):   
   	ubit = QtGui.QListWidgetItem(name)
        #ubit.setIcon(QtGui.QIcon(r"Pictures/grad_cap.gif"))
        ubit.setFont(QtGui.QFont('Verdana', 14,weight=12))
        self.addItem(ubit)

        
    def pop(self):
        return self.takeItem(0)
        #try:
        #    return self.findItems(name, QtCore.Qt.MatchExactly)[0] 
        #except IndexError:
        #    return False

        