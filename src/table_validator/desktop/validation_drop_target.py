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

import click
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

import table_validator

logger = logging.getLogger(__name__)

__all__ = [
    'ValidationDropTarget',
    'main',
]


class ValidationDropTarget(QWidget):
    """A Qt app that is a drop target and validates the file dropped."""

    def __init__(self, template_file):
        # self.labelUrl = 0;
        super().__init__()

        self.setAcceptDrops(True)
        self.initUI()

        self.template = table_validator.parse_tsv(template_file)

        # taken from
        # https://www.iana.org/assignments/media-types/media-types.txt
        self.accepted_formats = ['text/uri-list']

    def _validate_table(self, candidate) -> bool:
        return table_validator.validate(self.template, candidate)

    def dropEvent(self, e):  # noqa: N802
        """Handle file drop events."""
        logger.debug("Dropped!")
        urls = e.mimeData().urls()
        response = urllib.request.urlopen(urls[0].toString())  # noqa:S310
        candidate = table_validator.parse_tsv(response.read().decode("UTF-8").split("\n"))

        logger.debug("Candidate %s" % candidate)

        self.label_url.setText(urls[0].toString())

        if self._validate_table(candidate):
            self.label_success.setText(
                '<span style=" font-size:18pt; font-weight:600; color:#00aa00;">Validation succeeded!</span>')
        else:
            self.label_success.setText(
                '<span style=" font-size:18pt; font-weight:600; color:#8B0000;">Validation failed!</span>')

        logger.debug("dropped" % urls)

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

    def dragEnterEvent(self, e):  # noqa: N802
        """Decide if you can drop a given type of file in the drop zone."""
        logger.debug("enter")
        logger.debug(f'URLs: {e.mimeData().urls()}')

        accept = self.is_accepted(e)
        if accept:
            logger.debug("Accepted")
        else:
            logger.debug("failed %s" % e.mimeData().formats())

    def initUI(self):  # noqa: N802
        """Initialize the UI."""
        self.label_url = QLabel()
        self.label_url.setAlignment(Qt.AlignLeft)
        self.label_url.setText("Drop your files here:")

        self.label_success = QLabel()
        self.label_success.setAlignment(Qt.AlignLeft)
        self.label_success.setText("Not analyzed, yet!")

        self.label_instructions = QLabel()
        self.label_instructions.setAlignment(Qt.AlignLeft)
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
        self.setGeometry(800, 500, 300, 400)


@click.command()
@click.option('-t', '--template', type=click.File(), default='template.tsv')
@click.option('-v', '--verbose', is_flag=True)
def main(template, verbose: bool):
    """Run the table_validator Desktop App."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    click.echo(f'Building table validator with {template.name}')
    app = QApplication([])
    drop_target = ValidationDropTarget(template)
    drop_target.show()
    app.exec_()


if __name__ == '__main__':
    main()
