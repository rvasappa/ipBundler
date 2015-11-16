#!/usr/bin/env python3.4

import os,sys
from PyQt4 import QtGui, QtCore
import subprocess
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import tarfile

from tickUntickDir import *
from InputDialog import *

 
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        #self.model = QtGui.QFileSystemModel(self)
        self.model  = tickUntickDir() 
        self.status = QtGui.QStatusBar(self)

        self.palette = QtGui.QPalette()
        self.palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.green)
        self.status.showMessage("Ready")
        self.status.setPalette(self.palette)
        self.labelFileName = QtGui.QLabel(self)
        self.labelFileName.setText("Directory Name:")
        self.labelFileName.setPalette(self.palette)
        self.query = QtGui.QLineEdit(self)

     
        """
            Default is to start in user current directory
        """
        
        self.query.setText(os.environ['PWD'])

        self.labelFilePath = QtGui.QLabel(self)
        self.labelFilePath.setText("Search Pattern:")
        self.lineEditFilePath = QtGui.QLineEdit(self)
        self.lineEditFilePath.setDisabled(True)
        self.labelFilePath.setPalette(self.palette)
        
        self.buttonFileSearch = QtGui.QPushButton(self)
        self.buttonFileSearch.setText("Search")
        self.buttonFileSearch.clicked.connect(self.searchButton)
        self.query.returnPressed.connect(self.buttonFileSearch.click)
        self.query.setFocus()

        self.buttonGenBundle = QtGui.QPushButton(self)
        self.buttonGenBundle.setText("Generate Bundle")
        self.buttonGenBundle.clicked.connect(self.genBundleButton)
        self.buttonGenBundle.setStyleSheet("background-color: cyan")
        self.buttonGenBundle.setIcon(QtGui.QIcon('icons/tar-gz.png'))
        
        self.labelselectAllCB = QtGui.QLabel(self)
        self.labelselectAllCB.setText("SelectAll")
        self.labelselectAllCB.setPalette(self.palette)
        self.selectAllCB = QtGui.QCheckBox(self)
        self.selectAllCB.setGeometry(QtCore.QRect(50, 390, 71, 21))
        self.selectAllCB.setObjectName(_fromUtf8("SelectAll"))
        self.selectAllCB.clicked.connect(self.selectAll)
        
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
        self.setStyle()

    def setStyle(self):
        self.treeView.setStyleSheet("""
            QTreeView {
                show-decoration-selected: 1;
            }

            QTreeView::item {
                border: 1px solid #d9d9d9;
                border-top-color: transparent;
                border-bottom-color: transparent;
            }

            QTreeView::item:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
                border: 1px solid #bfcde4;
            }

            QTreeView::item:selected {
                border: 1px solid #567dbc;
            }

            QTreeView::item:selected:active{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
            }

            QTreeView::item:selected:!active {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
            }
            QTreeView::branch {
                background: palette(base);
            }

            QTreeView::branch:has-siblings:!adjoins-item {
                background: cyan;
            }

            QTreeView::branch:has-siblings:adjoins-item {
                background: orange;
            }

            QTreeView::branch:!has-children:!has-siblings:adjoins-item {
                background: blue;
            }

            QTreeView::branch:closed:has-children:has-siblings {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #33cc33, stop: 1 #33cc33); ;
            }

            QTreeView::branch:has-children:!has-siblings:closed {
                background: purple;
            }

            QTreeView::branch:open:has-children:has-siblings {
                background: violet;
            }

            QTreeView::branch:open:has-children:!has-siblings {
                background: green;
            }
            QLineEdit { background: yellow }
        """)

    def setMarkStyle(self):
        self.treeView.setStyleSheet("""
            
            QTreeView::item:selected {
                border: 1px solid red;
                background: green;
            }   
        """)
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
        self.treeView.setSortingEnabled(True)
        self.treeView.expandsOnDoubleClick()
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setColumnWidth(0, 200)
        self.treeView.sortByColumn(0, QtCore.Qt.AscendingOrder)

    def addToTreeHere(self):
        self.treeView.expand(self.treeView.currentIndex())
        fileName = self.model.fileName(self.treeView.currentIndex())
        filePath = self.model.filePath(self.treeView.currentIndex())
        if os.path.isdir (fileName):
            self.treeView.expand(self.treeView.currentIndex())
        elif os.path.isfile (filePath):
            print ("-Info- Opening File %s" %(filePath))
            self.editFile(filePath)

    def editFile(self,efile):
        os.environ.get('EDITOR') if os.environ.get('EDITOR') else 'gvim'
        edit_call = [ "gvim",efile]; 
        edit = subprocess.Popen(edit_call)

    def layout(self):
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.addWidget(self.labelFileName, 0, 0)
        self.gridLayout.addWidget(self.query, 0, 1)
        self.gridLayout.addWidget(self.labelFilePath, 1, 0)
        self.gridLayout.addWidget(self.lineEditFilePath, 1, 1)
        self.gridLayout.addWidget(self.labelselectAllCB, 0, 2)
        self.gridLayout.addWidget(self.selectAllCB, 0, 3)
        self.gridLayout.addWidget(self.buttonFileSearch, 1, 2)
        self.gridLayout.addWidget(self.buttonGenBundle, 1, 3)
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
            self.setStyle()
            self.status.showMessage("Ready")
        elif not os.path.isdir(Newpath):
            self.status.showMessage("-Error- Dude, this directory does not exist and you have increased my paranoia!")
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
                self.selIndex = index
                level += 1
        
        menu = QtGui.QMenu()
        menu.addAction("Mark/Unmark", self.open_treeObj)
        menu.exec_(self.treeView.viewport().mapToGlobal(position))
    
    def open_treeObj(self):
        index = self.treeView.selectedIndexes()[0]
        if (self.model.checkState(index)) < 1:
            self.model.setData(index,2, 10)
        else:
            self.model.setData(index,0, 10)



    def delete_treeObj(self):
        print ("Delete Object")
        root = self.treeView.invisibleRootItem()
        for item in self.selectedItems():
            (item.parent() or root).removeChild(item)
    
    def on_treeView_clicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        fileName = self.model.fileName(indexItem)
        filePath = self.model.filePath(indexItem)

    def selectAll(self):
        if self.selectAllCB.isChecked():
            self.treeView.selectAll()
            indexA = self.treeView.selectedIndexes()
            for index in indexA:
                if (self.model.checkState(index)) < 1:
                    self.model.setData(index,2, 10)
                    self.treeView.clearSelection()

        else:
            self.treeView.selectAll()
            indexA = self.treeView.selectedIndexes()
            for index in indexA:
                if (self.model.checkState(index)) > 1:
                    self.model.setData(index,0, 10)
                    self.treeView.clearSelection()

    def searchButton(self):
        print ("Starting Search")
        self.refreshTree()

    def genBundleButton(self):
        print ("Generating Bundle")
        indexA = self.treeView.selectedIndexes()
        if (self.model.checkState(indexA[0]) > 1):
            self.treeView.selectAll()
            tarBallInput = InputDialog(self, title="Enter Tar Bundle Name", label="Tarball Name", text="")
            tarBallInput.exec_()
            tarBall = tarBallInput.text.text()
            tFile = tarfile.open(tarBall, 'w:gz')
            
            for index in indexA:
                if (self.model.checkState(index)) >= 1:
                    indexItem = self.model.index(index.row(), 0, index.parent())
                    fileName = self.model.fileName(indexItem)
                    filePath = self.model.filePath(indexItem)
                    tFile.add(filePath)
            
            if len(tFile.getnames()) > 0:
                for f in tFile.getnames():
                    print ("Added %s" % f)
                
                self.treeView.clearSelection()
                tFile.close()
                print ("Finished Generating Bundle, Generated %s" %(tarBall))
                self.status.showMessage("Finished Generating Bundle")
                self.status.showMessage("Ready")
                

def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('IPBundler')
    form = MyWindow()
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Background,QtCore.Qt.black)
    form.setPalette(palette)
    form.resize(866, 333)
    form.move(app.desktop().screen().rect().center() - form.rect().center())
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
