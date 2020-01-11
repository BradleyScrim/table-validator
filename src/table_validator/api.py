# -*- coding: utf-8 -*-

"""API for ``table_validator``."""

import logging
import pandas as pd
from collections import defaultdict
from functools import partial
from typing import Any, Callable, Iterable, List, Mapping, Set, TextIO, Tuple, Union
from . import validator_classes as v

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



# TODO: Replace with objects
def parse_template(template) -> Rules:
    """Parse a template."""

    returnValue = []

    for i, row in enumerate(template):
        for j, cell in enumerate(row):
            if pd.isnull(cell):
                continue

            open_bracket = cell.find('{')
            if -1 == open_bracket:
                # no opening bracket
                # -- this means we have a string that should be reproduced
                print(f'{EMOJI} exact comparison at ({i}, {j}): {cell}')
                returnValue.append(v.ExactStringSheetValidator(i,j,cell))
            else:
                close_bracket = cell.find('}', open_bracket)
                if -1 == close_bracket:
                    raise ValueError(f'ERROR in {i}, {j} {cell}: no right bracket')

                command = cell[open_bracket + 1: close_bracket]
                # print(f'{EMOJI} command at ({i}, {j}): {command}')

                # TODO: here we have to create the right NEW validators
                if command.startswith('INT'):
                    returnValue.append(v.MandatorySheetValidator(i,j))
                    returnValue.append(v.IntTypeSheetValidator(i, j))
                elif command.startswith('FLOAT'):
                    returnValue.append(v.MandatorySheetValidator(i, j))
                    returnValue.append(v.FloatTypeSheetValidator(i, j))
                elif command.startswith('STR'):
                    returnValue.append(v.MandatorySheetValidator(i, j))
                #elif
                #    True
                    #command.startswith('REPEAT_ROW'):
                    #yield 'REPEAT', i


    yield returnValue
    return returnValue


def _consume_parsed_template(rules: Rules) -> Tuple[Mapping[int, Mapping[int, List[Validator]]], Set[int]]:
    """Reorganize the parsed template."""
    rule_dict = defaultdict(lambda: defaultdict(list))
    for rule in rules:
        for o in rule:
            # print(o)
            rule_dict[o.row][o.column].append(o)

    rule_dict = {k: dict(v) for k, v in rule_dict.items()}
    #print(rule_dict, '{EMOJI} rules')
    return rule_dict, None



def old_validate(template: List[List[Any]], candidate: List[List[Any]]) -> Tuple[bool,List[Any]]:
    """Validate a candidate using a given template."""
    rules, repeats = _consume_parsed_template(parse_template(template))

    current_row_index = 0

    errors = []

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
                print("§ VALIDATOR %s",validator)
                (v,e) = validator.validate(candidate[current_row_index][current_column_index])
                if(v):
                    continue
                else:
                    errors.append(e)

            current_column_index += 1
        current_row_index += 1
    return (len(errors)==0),errors

def validate(template: List[List[Any]], candidate: List[List[Any]]) -> Tuple[bool,List[Any]]:
    """Validate a candidate using a given template."""
    parse_result = parse_template(template)
    #print("PARSE RESULT %s" % parse_result )
    rules, repeats = _consume_parsed_template(parse_result)

    current_row_index = 0

    errors = []

    #print("TEMPLATE:")
    #print(rules)

    for current_row_index, row in rules.items():
        # print("current_row_index %s" % current_row_index)
        # print("Row %s" % row)
        for current_column_index, validators in row.items():
            for validator in validators:
                value = None
                try:
                    value = candidate[current_row_index][current_column_index]
                except:
                    value = None
                # print("Validator %s" % validator)
                (v,e) = validator.validate(value)
                if(v):
                    continue
                else:
                    errors.append(e)

    return (len(errors)==0),errors

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
