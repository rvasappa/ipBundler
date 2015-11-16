#!/usr/bin/env python3.4

import os,sys
from PyQt4 import QtGui, QtCore
import subprocess
from PyQt4.QtGui import *
from PyQt4.QtCore import *


from search import SearchThread


class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.model = QtGui.QFileSystemModel(self)
        self.status = QtGui.QStatusBar(self)
        self.status.showMessage("Ready")
        self.labelFileName = QtGui.QLabel(self)
        self.labelFileName.setText("Directory Name:")
        self.query = QtGui.QLineEdit(self)
        
        """
            Default is to start in user current directory
        """
        
        self.query.setText(os.environ['PWD'])

        self.labelFilePath = QtGui.QLabel(self)
        self.labelFilePath.setText("Search Pattern:")
        self.lineEditFilePath = QtGui.QLineEdit(self)
        
        self.buttonFileSearch = QtGui.QPushButton(self)
        self.buttonFileSearch.setText("Search")
        self.buttonFileSearch.clicked.connect(self.searchButton)
        self.query.returnPressed.connect(self.buttonFileSearch.click)
        self.query.setFocus()
        path = self.query.text()
        self.initpath = path
        self.initTree()

    def initTree(self):
        print (self.initpath)
        self.model.setRootPath(self.initpath)
        self.model.setReadOnly(False)
        self.indexRoot = self.model.index(self.model.rootPath())
        self.treeView = QtGui.QTreeView(self)
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.indexRoot)
        self.treeProps()
        self.layout()

    def treeProps(self):
        self.treeView.clicked.connect(self.on_treeView_clicked)
        self.treeView.setDragEnabled(True)
        self.treeView.setAcceptDrops(True)
        self.treeView.setDropIndicatorShown(True)
        self.treeView.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.treeView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)
        self.treeView.doubleClicked.connect(self.addToTreeHere)

    def addToTreeHere(self):
        print ("Item has been double clicked...")
        
    def layout(self):
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.addWidget(self.labelFileName, 0, 0)
        self.gridLayout.addWidget(self.query, 0, 1)
        self.gridLayout.addWidget(self.labelFilePath, 1, 0)
        self.gridLayout.addWidget(self.lineEditFilePath, 1, 1)
        self.gridLayout.addWidget(self.buttonFileSearch, 1, 2)
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addLayout(self.gridLayout)
        self.layout.addWidget(self.treeView)
        self.layout.addWidget(self.status)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)


    def relayout(self):
        layout = self.layout
        if layout != None:
            self.treeViewWidget = self.layout.addWidget(self.treeView)
            self.layout.addWidget(self.status)


    def refreshTree(self):
        Newpath = self.query.text()
        if Newpath != self.initpath and os.path.isdir(Newpath):
            print (Newpath)
            self.status.showMessage("Searching...")

            self.treeView.deleteLater()
            self.treeView.setParent(None)
            self.status.setParent(None)
            self.initpath = Newpath
            self.model.setRootPath(self.initpath)
            self.model.setReadOnly(False)
            self.indexRoot = self.model.index(self.model.rootPath())
            self.treeView = QtGui.QTreeView(self)
            self.treeView.setModel(self.model)
            self.treeView.setRootIndex(self.indexRoot)
            self.treeProps()
            self.relayout()
            self.status.showMessage("Ready")
        elif not os.path.isdir(Newpath):
            self.status.showMessage("-Error- Dude, this directory does not exist")
        else:
            self.status.showMessage("Ready.")






    

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
        menu.addAction("Open", self.open_treeObj)
        menu.addAction("Delete", self.delete_treeObj)
        menu.exec_(self.treeView.viewport().mapToGlobal(position))
    
    def open_treeObj(self):
        print ("Open Object")
        self.ff.show()
    
    def delete_treeObj(self):
        print ("Delete Object")
        root = self.treeView.invisibleRootItem()
        for item in self.selectedItems():
            (item.parent() or root).removeChild(item)
    
    def on_treeView_clicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        fileName = self.model.fileName(indexItem)
        filePath = self.model.filePath(indexItem)


    def searchButton(self):
        print ("Starting Search")
        self.refreshTree()


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
