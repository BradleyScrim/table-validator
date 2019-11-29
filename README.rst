table-validator
===============
Use tables with validation schemata to validate other tables.

Dependencies
------------
- INFO: Source Code of the Compund Parser by Lukrécia Mertová: https://github.com/mertova/Compound_parser_hackethon2019

Installation
------------
Install directly from `GitHub <https://github.com/cthoyt/table-validator>`_ with:

.. code-block:: sh

   $ pip install git+https://github.com/cthoyt/table-validator.git

Testing
-------
Install ``tox`` with ``pip install tox`` then run with ``tox``.

Usage
-----
Desktop Usage
~~~~~~~~~~~~~
To run the desktop interface, you also need to install the ``PyQt5`` package with ``pip`` then run:

.. code-block:: sh

   $ python -m table_validator.desktop

The ``--template`` option can specify a template file other than ``template.tsv`` in the current directory.

Web Usage
~~~~~~~~~
To run the web interface, you also need to run

.. code-block:: sh

   $ pip install flask flask-wtf flask-bootstrap

then run

.. code-block:: sh

   $ python -m table_validator.web

The ``--template`` option can specify a template file other than ``template.tsv`` in the current directory.

CLI Usage
~~~~~~~~~
Installation with ``pip`` adds a command ``table_validator`` that takes two arguments: a path to the template file,
and a path to the candidate file. Given files ``template.tsv`` and ``candidate.tsv``:

.. code-block:: tsv

    # template.tsv
    	C_A C_B C_C
    R_1 {INT(REQUIRED=TRUE)}	{INT(REQUIRED=TRUE)}	{INT(REQUIRED=TRUE)}

.. code-block:: tsv

    # candidate.tsv
    	C_A C_B C_C
    R_1 1	2	3

You can run:

.. code-block:: sh

    $ table_validator template.tsv candidate.tsv
