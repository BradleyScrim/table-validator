#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QHBoxLayout, QHeaderView, QSizePolicy,
                               QTableView, QWidget)
from PyQt5 import QtCore, QtGui

class FullCandidateTableModel(QAbstractTableModel):
    COLUMNS = [
        ("Location"),
        ("Value"),
        ("Error Message"),
    ]
    def __init__(self, data=None, parent=None):
        QAbstractTableModel.__init__(self,parent)
        self.load_data(data)

    def load_data(self, data):
        self.layoutAboutToBeChanged.emit()
        if data is None:
            data=[]
        self.__data = data

        # update view
        self.layoutChanged.emit()
        self.headerDataChanged.emit(Qt.Horizontal, 0, self.columnCount())
        self.headerDataChanged.emit(Qt.Vertical, 0, self.rowCount())
        self.dataChanged.emit(self.index(0, 0),
                              self.index(self.rowCount() - 1,
                                         self.columnCount() - 1))


    def rowCount(self, parent=QModelIndex()):
        return len(self.__data)

    def columnCount(self, parent=QModelIndex()):
        if(self.__data and self.__data[0]):
            return len(self.__data[0])
        else:
            return 0

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.COLUMNS[section]
        else:
            return "{}".format(section)

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            if(row<len(self.__data) and column<len(self.__data[row])):
                return "%s" % self.__data[row][column]
            else:
                return "x"

        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None

class FullCandidateTableWidget(QWidget):

    def load_data(self,data):
        self.model.load_data(data)

    def __init__(self, data=None):
        QWidget.__init__(self)

        # Getting the Model
        self.model = FullCandidateTableModel(data,self)

        # Creating a QTableView
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        # QTableView Headers
        self.horizontal_header = self.table_view.horizontalHeader()
        self.vertical_header = self.table_view.verticalHeader()
        self.horizontal_header.setSectionResizeMode(
                               QHeaderView.ResizeToContents
                               )
        self.vertical_header.setSectionResizeMode(
                             QHeaderView.ResizeToContents
                             )
        self.horizontal_header.setStretchLastSection(True)

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        ## Left layout
        size.setHorizontalStretch(1)
        self.table_view.setSizePolicy(size)
        self.main_layout.addWidget(self.table_view)
        self.table_view.setSelectionBehavior(QTableView.SelectItems)
        # Set the layout to the QWidget
        self.setLayout(self.main_layout)
