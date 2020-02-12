#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Desktop GUI for ``table_validator``.

Author: Wolfgang Müller
The initial starting point was taken from zetcode
However, there are only few lines that survived changes.

-
ZetCode PyQt5 tutorial

This is a simple drag and
drop example.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017

http://zetcode.com/gui/pyqt5/dragdrop/
"""

import logging
import sys
import urllib.request
from typing import Type

import click
from PyQt5.QtCore import QPropertyAnimation, QRect, Qt,QItemSelection,QItemSelectionModel,QModelIndex
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QGridLayout, QWidget
from PyQt5.QtGui import QBrush
from .candidate_table import CandidateTableWidget, CandidateTableModel
from .full_candidate_table import FullCandidateTableWidget, FullCandidateTableModel

import table_validator
from PyQt5.Qt import QEvent, QPushButton

logger = logging.getLogger(__name__)

__all__ = [
    'ValidationDropTarget',
    'main',
]


class ValidationOverview(QWidget):
    """A Qt window showing the file and error messages"""

    def __init__(self, app, candidate, new_table_data, errors_encountered):
        # self.label_url = 0
        super().__init__()

        self.errors_encountered = errors_encountered
        # init tables
        self.full_candidate_table_widget = FullCandidateTableWidget()
        self.candidate_table_widget = CandidateTableWidget()
        self.candidate_table_widget.table_view.selectRow(0)
        self.full_candidate_table_widget.model.load_data(candidate)
        self.candidate_table_widget.model.load_data(new_table_data)
        self.close_button = QPushButton("close window")
        self.close_button.clicked.connect(self.closeWindow)

        # init window
        self.app = app
        desktop = app.desktop()
        geometry = desktop.availableGeometry()
        self.top = geometry.top()
        self.left = geometry.left()
        self.initUI()
        self._big_geometry()

    def closeWindow(self):
        self.destroy()

    def _big_geometry(self):
        self.setFixedSize(self.GEOMETRY_W, self.GEOMETRY_H)

    def view_clicked(self, clicked_index):
        print("clicked:",clicked_index.row())

        #self.full_candidate_table_widget.table_view.selectRow(clicked_index.row())

        model = self.full_candidate_table_widget.table_view.selectionModel()
        #print("------");
        #print(dir(self.full_candidate_table_widget.table_view.model()))
        #print("------");
        #print(self.full_candidate_table_widget.table_view.model())
        #print("------");

        (row, col) = self.errors_encountered[clicked_index.row()].get_location()

        index = self.full_candidate_table_widget.table_view.model().index(row,col)
        model.select(QItemSelection(index,index),QItemSelectionModel.Select | QItemSelectionModel.Clear)

    # initUI
    def initUI(self):

        self.GEOMETRY_W = 800
        self.GEOMETRY_H = 600
        self.GEOMETRY_X = 10
        self.GEOMETRY_Y = 10 

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        vbox = QGridLayout()

        vbox.addWidget(self.full_candidate_table_widget,0,0)
        vbox.addWidget(self.candidate_table_widget,1,0)
        vbox.addWidget(self.close_button,2,0)

        self.bottom = self.app.desktop().availableGeometry().bottom()
        total_height = self.bottom * 0.8
        content_height = total_height * 0.6

        vbox.setRowMinimumHeight(0,content_height)

        self.setLayout(vbox)

        self.setWindowTitle('INCOME table Validation result')

        # connect to line
        self.candidate_table_widget.defineTableClickedListener(self.view_clicked)


class ValidationDropTarget(QWidget):
    """A Qt app that is a drop target and validates the file dropped."""

    def __init__(self, app, validate):
        
        self.__change_size=False
        
        self.errors_encountered = []
        self.label_url = QLabel()
        self.label_success = QLabel()
        self.label_instructions = QLabel()
        self.close_button = QPushButton("close application")
        self.close_button.clicked.connect(self.destroy)

        # self.label_url = 0
        super().__init__()

        self.app = app
        desktop = app.desktop()
        geometry = desktop.availableGeometry()
        self.bottom = geometry.bottom()
        self.right = geometry.right()
        self.setAcceptDrops(True)
        self.initUI()

        self.validate = validate
        
        self.validation_overview_window=None

        # taken from
        # https://www.iana.org/assignments/media-types/media-types.txt
        self.accepted_formats = ['text/uri-list']

    def _big_geometry(self):
        if (self.x() < self.GEOMETRY_X) and (self.y() < self.GEOMETRY_Y):
            return

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(self.GEOMETRY_ANIMATION_TIME)
        self.animation.setStartValue(QRect(self.GEOMETRY_X, self.GEOMETRY_Y, self.GEOMETRY_W, self.GEOMETRY_H))
        self.animation.setEndValue(QRect(self.GEOMETRY_BIG_X, self.GEOMETRY_BIG_Y, self.GEOMETRY_BIG_W, self.GEOMETRY_BIG_H))
        self.animation.start()
        self.setFixedSize(self.GEOMETRY_BIG_W, self.GEOMETRY_BIG_H)


    def _small_geometry(self):
        if (self.x() == self.GEOMETRY_X) and (self.y() == self.GEOMETRY_Y):
            return

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(self.GEOMETRY_ANIMATION_TIME)
        self.animation.setStartValue(QRect(self.GEOMETRY_BIG_X, self.GEOMETRY_BIG_Y, self.GEOMETRY_BIG_W, self.GEOMETRY_BIG_H))
        self.animation.setEndValue(QRect(self.GEOMETRY_X, self.GEOMETRY_Y, self.GEOMETRY_W, self.GEOMETRY_H))
        self.animation.start()
        self.setFixedSize(self.GEOMETRY_BIG_W, self.GEOMETRY_BIG_H)

    @staticmethod
    def preprocess_response(data):
        return table_validator.parse_tsv(data.split("\n"))

    def dropEvent(self, e):  # noqa: N802
        """Handle file drop events."""
        logger.debug("Dropped!")
        
        urls = e.mimeData().urls()
        response = urllib.request.urlopen(urls[0].toString())  # noqa:S310
        data = response.read().decode("UTF-8")
        candidate = self.preprocess_response(data)


        logger.debug("Candidate %s", candidate)

        self.label_url.setText("File examined: %s" % urls[0].toString())

        successfullyValidated,errorObjects = self.validate(candidate)

        self.errors_encountered = errorObjects;
        new_table_data=[]
        for i in errorObjects:
            # object is SheetError
            print(i.get_formatted_full_error_message())
            new_table_data.append(i)


        self.label_instructions.hide()
        if successfullyValidated:
            self.label_success.setText(
                '<span style=" font-size:18pt; font-weight:600; color:#00aa00;">'
                'Validation succeeded!'
                '</span>'
            )
        else:
            self.label_success.setText(
                '<span style=" font-size:18pt; font-weight:600; color:#cc0000;">'
                """
                Validation failed. Please browse errors using the error list.
                The locations of the error occurrences will be marked.
                """
                '</span>'
            )
            
            # create/update overview table
            self.validation_overview_window = ValidationOverview(self.app, candidate, new_table_data, self.errors_encountered)
            self.validation_overview_window.show()

        logger.debug("dropped %s", urls)
        # self._small_geometry()

    def is_accepted(self, e):
        """Check a file based on its MIME type."""
        accept = any(
            e.mimeData().hasFormat(i)
            for i in self.accepted_formats
        )

        if accept:
            e.accept()
            return True
        else:
            e.ignore()

        return False

    def enterEvent(self, e):
        if self.__change_size:
            self._big_geometry()

    def leaveEvent(self, e):
        if self.__change_size:
            self._small_geometry()

    def dragEnterEvent(self, e):  # noqa: N802
        """Decide if you can drop a given type of file in the drop zone."""
        if self.__change_size:
            self._big_geometry()

        logger.debug("enter")
        logger.debug("URLs: %s", e.mimeData().urls())

        if self.is_accepted(e):
            logger.debug("Accepted")
        else:
            logger.debug("failed %s", e.mimeData().formats())

    # initUI
    def initUI(self):

        self.GEOMETRY_W = 30
        self.GEOMETRY_H = 30
        self.GEOMETRY_X = self.right - self.GEOMETRY_W
        self.GEOMETRY_Y = self.bottom - self.GEOMETRY_H
        self.GEOMETRY_BIG_W = 400
        self.GEOMETRY_BIG_H = 300
        self.GEOMETRY_BIG_X = self.right - self.GEOMETRY_BIG_W
        self.GEOMETRY_BIG_Y = self.bottom - self.GEOMETRY_BIG_H
        self.GEOMETRY_ANIMATION_TIME = 0

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self._small_geometry()
        # https://stackoverflow.com/questions/18975734/how-can-i-find-the-screen-desktop-size-in-qt-so-i-can-display-a-desktop-notific

        self.label_url.setAlignment(Qt.AlignLeft)
        self.label_url.setWordWrap(True)
        self.label_url.setText("Drop your files here:")

        self.label_success.setAlignment(Qt.AlignLeft)
        self.label_success.setText('<span style="color:#999999;">I did not yet analyze any file</span>')

        self.label_instructions.setAlignment(Qt.AlignLeft)
        self.label_instructions.setWordWrap(True)
        self.label_instructions.setText("""
        <p>
        Are you asking yourself if your tabular data file is really matching
        the template you agreed on with your collaboration partners?
        <p>
        Then this tool is the solution for you. Just take this file in your
        file manager (finder, windows explorer, nautilus...) and then
        <b> drop it</b> onto this window.
        <p>
        We will check the format compliance of your file and immediately
        give
        <ul>
        <li> information if it is correct with respect to the template
        <li> give information on where it is incorrect
        </ul>

        <p>
        <b>Note:</b> Currently we process only <b>tab delimited</b> files.
        </p>
        """)

        vbox = QGridLayout()

        vbox.addWidget(self.label_url,1,0)
        vbox.addWidget(self.label_success,2,0)
        vbox.addWidget(self.label_instructions,3,0)
        vbox.addWidget(self.close_button,4,0)
        #vbox.addStretch()

        total_height = self.bottom * 0.8
        content_height = total_height * 0.6

        vbox.setRowMinimumHeight(0,content_height)

        self.setLayout(vbox)

        self.setWindowTitle('INCOME table Validation Drop Target')
        # self.setGeometry(800, 500, 300, 400)

def run_with_validator(
        validate,
        cls: Type[ValidationDropTarget] = None,
) -> None:
    if cls is None:
        cls = ValidationDropTarget

    app = QApplication([])

    drop_target = cls(app, validate)
    drop_target.show()
    return app.exec_()


@click.command()
@click.option('-t', '--template', type=click.File(), default='template.tsv')
@click.option('-v', '--verbose', is_flag=True)
def main(template, verbose: bool):
    """Run the table_validator Desktop App."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        print("start with template",template)

    click.echo(f'Building table validator with {template.name}')
    validate = table_validator.TemplateValidator(template)
    sys.exit(run_with_validator(validate))


if __name__ == '__main__':
    main()
