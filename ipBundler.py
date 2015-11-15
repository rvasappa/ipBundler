#!/usr/bin/env python3.4

import sys
from PyQt4 import QtGui, QtCore



class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.model = QtGui.QFileSystemModel(self)
        path = "/home/raghuram002/development/src/code"
        self.model.setRootPath(path)
        self.model.setReadOnly(False)
        self.indexRoot = self.model.index(self.model.rootPath())
        self.treeView = QtGui.QTreeView(self)
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.indexRoot)
        self.treeView.clicked.connect(self.on_treeView_clicked)
        self.treeView.setDragEnabled(True)
        self.treeView.setAcceptDrops(True)
        self.treeView.setDropIndicatorShown(True)
        self.treeView.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.treeView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)
        
        self.labelFileName = QtGui.QLabel(self)
        self.labelFileName.setText("File Name:")

        self.lineEditFileName = QtGui.QLineEdit(self)

        self.labelFilePath = QtGui.QLabel(self)
        self.labelFilePath.setText("File Path:")

        self.lineEditFilePath = QtGui.QLineEdit(self)

        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.addWidget(self.labelFileName, 0, 0)
        self.gridLayout.addWidget(self.lineEditFileName, 0, 1)
        self.gridLayout.addWidget(self.labelFilePath, 1, 0)
        self.gridLayout.addWidget(self.lineEditFilePath, 1, 1)
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addLayout(self.gridLayout)
        self.layout.addWidget(self.treeView)

    

    @QtCore.pyqtSlot(QtCore.QModelIndex)
     
    def openMenu(self, position):
        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        
        menu = QtGui.QMenu()
        menu.addAction(self.tr("Edit object"))
        menu.addAction(self.tr("Delete object"))
        menu.exec_(self.treeView.viewport().mapToGlobal(position))
    
    def on_treeView_clicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())

        fileName = self.model.fileName(indexItem)
        filePath = self.model.filePath(indexItem)

        self.lineEditFileName.setText(fileName)
        self.lineEditFilePath.setText(filePath)


def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('IPBundler')
    form = MyWindow()
    form.resize(866, 333)
    form.move(app.desktop().screen().rect().center() - form.rect().center())
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
