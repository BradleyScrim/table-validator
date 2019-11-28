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
import urllib.request
from typing import Type

import click
from PyQt5.QtCore import QPropertyAnimation, QRect, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

import table_validator

logger = logging.getLogger(__name__)

__all__ = [
    'ValidationDropTarget',
    'main',
]


class ValidationDropTarget(QWidget):
    """A Qt app that is a drop target and validates the file dropped."""

    def __init__(self, app, validate, bottom, right):
        self.label_url = QLabel()
        self.label_success = QLabel()
        self.label_instructions = QLabel()

        # self.label_url = 0
        super().__init__()

        self.app = app
        self.bottom = bottom
        self.right = right
        self.setAcceptDrops(True)
        self.initUI()

        self.validate = validate

        # taken from
        # https://www.iana.org/assignments/media-types/media-types.txt
        self.accepted_formats = ['text/uri-list']

    def _big_geometry(self):
        w = 30
        h = 30
        x = self.right - w
        y = self.bottom - h

        big_w = 300
        big_h = 300
        big_x = self.right - big_w
        big_y = self.bottom - big_h

        if (self.x() < x) and (self.y() < y):
            return

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(250)
        self.animation.setStartValue(QRect(x, y, w, h))
        self.animation.setEndValue(QRect(big_x, big_y, big_w, big_h))
        self.animation.start()
        self.setFixedSize(big_w, big_h)

    def _small_geometry(self):
        w = 30
        h = 30
        x = self.right - w
        y = self.bottom - h

        big_w = 300
        big_h = 300
        big_x = self.right - big_w
        big_y = self.bottom - big_h

        if (self.x() == x) and (self.y() == y):
            return

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(250)
        self.animation.setStartValue(QRect(big_x, big_y, big_w, big_h))
        self.animation.setEndValue(QRect(x, y, w, h))
        self.animation.start()
        self.setFixedSize(big_w, big_h)

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

        logger.debug("Candidate %s" % candidate)

        self.label_url.setText("File examined: %s" % urls[0].toString())

        successfullyValidated,errorObjects = self.validate(candidate)

        for i in errorObjects:
            print(i.message())

        if successfullyValidated:
            self.label_success.setText(
                '<span style=" font-size:18pt; font-weight:600; color:#00aa00;">'
                'Validation succeeded!'
                '</span>'
            )
        else:
            self.label_success.setText(
                '<span style=" font-size:18pt; font-weight:600; color:#cc0000;">'
                'Your data surely is great, but...'
                '</span>'
            )

        logger.debug("dropped" % urls)
        # self._small_geometry()

    def is_accepted(self, e):
        """Check a file based on its MIME type."""
        accept = any(
            e.mimeData().hasFormat(i)
            for i in self.accepted_formats
        )

        if accept:
            e.accept()
        else:
            e.ignore()

    def enterEvent(self, e):
        self._big_geometry()

    def leaveEvent(self, e):
        self._small_geometry()

    def dragEnterEvent(self, e):  # noqa: N802
        """Decide if you can drop a given type of file in the drop zone."""
        self._big_geometry()

        logger.debug("enter")
        logger.debug(f'URLs: {e.mimeData().urls()}')

        accept = self.is_accepted(e)
        if accept:
            logger.debug("Accepted")
        else:
            logger.debug("failed %s" % e.mimeData().formats())

    # initUI
    def initUI(self):
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

        vbox = QVBoxLayout()
        vbox.addWidget(self.label_url)
        vbox.addWidget(self.label_success)
        vbox.addWidget(self.label_instructions)
        vbox.addStretch()

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

    desktop = app.desktop()
    geometry = desktop.availableGeometry()
    bottom = geometry.bottom()
    right = geometry.right()

    drop_target = cls(app, validate, bottom, right)
    drop_target.show()
    app.exec_()


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
    run_with_validator(validate)


if __name__ == '__main__':
    main()
