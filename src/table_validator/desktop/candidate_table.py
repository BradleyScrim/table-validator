#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QHBoxLayout, QHeaderView, QSizePolicy,
                               QTableView, QWidget)

# TODO: this file needs a refactoring

class CandidateTableModel(QAbstractTableModel):
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
        return len(self.COLUMNS)

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

            if column==0:
                return self.__data[row].get_formatted_location()
            elif column==1:
                return self.__data[row].actual_value
            elif column==2:
                return self.__data[row].get_message()


        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None

class CandidateTableWidget(QWidget):
    def __init__(self, data=None):
        QWidget.__init__(self)

        # Getting the Model
        self.model = CandidateTableModel(data,self)

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

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)
