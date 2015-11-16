#!/usr/bin/env python3.4

from PyQt4 import QtGui, QtCore

class tickUntickDir(QtGui.QFileSystemModel):
    def __init__(self, parent=None):
        QtGui.QFileSystemModel.__init__(self, None)
        self.checks = {}
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.CheckStateRole:
            return QtGui.QFileSystemModel.data(self, index, role)
        else:
            if index.column() == 0:
                return self.checkState(index)
    
    def flags(self, index):
        return QtGui.QFileSystemModel.flags(self, index) | QtCore.Qt.ItemIsUserCheckable
    
    def checkState(self, index):
        if index in self.checks:
            return self.checks[index]
        else:
            return QtCore.Qt.Unchecked
    
    def setData(self, index, value, role):
        if (role == QtCore.Qt.CheckStateRole and index.column() == 0):
            self.checks[index] = value
            self.emit(QtCore.SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
            return True 
    
        return QtGui.QFileSystemModel.setData(self, index, value, role)
