# -*- coding: utf-8 -*-

"""API for ``table_validator``."""

import logging
from collections import defaultdict
from functools import partial
from typing import Any, Callable, Iterable, List, Mapping, Set, TextIO, Tuple, Union

import pandas as pd

logger = logging.getLogger(__name__)

EMOJI = '🔶'

DATA_TYPES = {
    'INT': int,
    'STR': str,
    'FLOAT': float,
}

Validator = Callable[[List[List[Any]], int, int], bool]
ValidatorTuple = Tuple[Validator, int, int]
Rules = Iterable[Union[List[ValidatorTuple], str]]

# What do we want to give back?
# One possibility: A message.
#       Advantage: simple
#       Drawback: Difficult to base other work on
#       My suggestion: Start with a message, change later
# Compromise:
# ErrorObject to create  a message

class SheetError:
    def __init__(self,row,column,value):
        self.row = row;
        self.column = column
        self.value = value

    def message(self):
        return "%d, %d: %s" %(row,column,value)

# TODO: Add classes for each validator

class TypeSheetError(SheetError):
    def __init__(self,row,column,value,cls):
        super(self,row,column,value)
        self.cls = cls

    def message(self):
        return "%d, %d: %s should have been of type %s" %(row,column,value,cls)


# base class
class SheetValidator:

    def __init__(self,row,column):
            self.row = row
            self.column = column
    # the location this is responsible for in the sheet
    def getLocation(self):
        return self.row,self.column

    # this does the actual validation
    # this empty validator always succeeds
    def validate(self,value):
        return True,SheetError(row,column,value)

class MandatorySheetValidator(SheetValidator):
# TODO a non-null value must be present
    def __init__(self,row,column):
        super(self,row,column)

    def validate(self):
        return True;SheetError(row,column,value)


class TypeSheetValidator(SheetValidator):
# TODO an integer/float/string must be present
    def something():
        return 0

class SmartChemicalCompoundSheetValidator(SheetValidator):
# TODO checks that something is a compound
    def somethingElse():
        return 0


# TODO: Replace with objects
def parse_template(template) -> Rules:
    """Parse a template."""
    for i, row in enumerate(template):
        for j, cell in enumerate(row):
            if pd.isnull(cell):
                continue

            open_bracket = cell.find('{')
            if -1 == open_bracket:
                continue

            close_bracket = cell.find('}', open_bracket)
            if -1 == close_bracket:
                raise ValueError(f'ERROR in {i}, {j} {cell}: no right bracket')

            command = cell[open_bracket + 1: close_bracket]
            print(f'{EMOJI} command at ({i}, {j}): {command}')

            # TODO: here we have to create the right NEW validators
            if command.startswith('INT'):
                yield [
                    (required_validator, i, j),
                    (int_validator, i, j),
                ]
            elif command.startswith('FLOAT'):
                yield [
                    (required_validator, i, j),
                    (float_validator, i, j),
                ]
            elif command.startswith('STR'):
                yield [(required_validator, i, j)]
            elif command.startswith('REPEAT_ROW'):
                yield 'REPEAT', i


def _consume_parsed_template(rules: Rules) -> Tuple[Mapping[int, Mapping[int, List[Validator]]], Set[int]]:
    """Reorganize the parsed template."""
    rule_dict = defaultdict(lambda: defaultdict(list))
    repeats = set()
    for rule in rules:
        if isinstance(rule, str):
            _, line = rule
            repeats.add(line)
        elif isinstance(rule, list):
            for v, i, j in rule:
                rule_dict[i][j].append(v)

    rule_dict = {k: dict(v) for k, v in rule_dict.items()}
    print( repeats, '{EMOJI} repeats')
    print(rule_dict, '{EMOJI} rules')
    return rule_dict, repeats


def required_validator(candidate: List[List[Any]], row: int, column: int) -> bool:
    """Validate a cell for existence."""
    _row = candidate[row]
    return _row[column]


def type_validator(candidate: List[List[Any]], row: int, column: int, cls: type) -> bool:
    """Validate a cell for having the given type."""
    value = candidate[row][column]

    try:
        cls(value)
    except ValueError:
        return False,ValidationErrorObject(row,column,"Wrong data type. Expected:", cls)
    else:
        return True


int_validator = partial(type_validator, cls=int)
float_validator = partial(type_validator, cls=float)


def validate(template: List[List[Any]], candidate: List[List[Any]]) -> Tuple[bool,List[Any]]:
    """Validate a candidate using a given template."""
    rules, repeats = _consume_parsed_template(parse_template(template))

    current_row_index = 0
    while current_row_index <= len(candidate):
        current_row_rules = rules.get(current_row_index)
        if current_row_rules is None:
            current_row_index += 1
            continue

        current_column_index = 0
        try:
            current_row = candidate[current_row_index]
        except IndexError:
            print('current row index', current_row_index)
            raise

        while current_column_index <= len(current_row):
            validators = current_row_rules.get(current_column_index)
            if validators is None:
                current_column_index += 1
                continue

            for validator in validators:
                if not validator(candidate, current_row_index, current_column_index):
                    return False,[]

            current_column_index += 1
        current_row_index += 1
    return True,[]

    # passed = True
    # row_offset = 0
    #
    # for rule in rules:
    #     if isinstance(rule, list):
    #         # multiple validations
    #         for validator, row, column in rule:
    #             if not validator(candidate, row, column):
    #                 print(f'failed at ({row}, {column}, {candidate[row][column]}: {validator}')
    #                 passed = False
    #                 break
    #     elif isinstance(rule, str):
    #         pass  # keep going until one row fails
    #         inner_passed = True
    #         while inner_passed:
    #             break
    #
    #     elif not rule(candidate, row, column):
    #         print(f'failed at ({row}, {column}, {candidate[row][column]}: {validator}')
    #         passed = False
    #
    # return passed


def parse_tsv(file: TextIO) -> List[List[str]]:
    """Parse a TSV file into a list of lists of strings."""
    return [
        list(line.strip().split('\t'))
        for line in file
    ]


if __name__ == '__main__':
    with open('os.path.dirname(os.path.abspath(__file__))' + '/tests/repeat_template.tsv') as _file:
        for x in parse_template(parse_tsv(_file)):
            print(x)
