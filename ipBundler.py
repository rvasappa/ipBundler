#!/usr/bin/env python3.4

import sys
from PyQt4 import QtGui, QtCore

data = [
    ("Alice", [
        ("Keys", []),
        ("Purse", [
            ("Cellphone", [])
            ])
        ]),
    ("Bob", [
        ("Wallet", [
            ("Credit card", []),
            ("Money", [])
            ])
        ])
    ]


class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels([self.tr("Contents")])
        """
        Idea is to add a json stream here
        """
        self.addItems(self.model, data)


        self.view = QtGui.QTreeView()
        self.view.setModel(self.model)
        self.view.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.setCentralWidget(self.view)
        self.view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.openMenu)
       
    def addItems(self, parent, elements):
        for text, children in elements:
            item = QtGui.QStandardItem(text)
            parent.appendRow(item)
            if children:
                self.addItems(item, children)
     
    def openMenu(self, position):
        indexes = self.view.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        
        menu = QtGui.QMenu()
        if level == 0:
            menu.addAction(self.tr("Edit person"))
        elif level == 1:
            menu.addAction(self.tr("Edit object/container"))
        elif level == 2:
            menu.addAction(self.tr("Edit object"))
        
        menu.exec_(self.view.viewport().mapToGlobal(position))


def main():
    app = QtGui.QApplication(sys.argv)
    form = MainForm()
    form.setWindowTitle('IPBundler')
    form.resize(666, 333)
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
