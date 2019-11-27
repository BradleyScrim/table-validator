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
    print(f'{EMOJI} repeats', repeats)
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
        return False
    else:
        return True


int_validator = partial(type_validator, cls=int)
float_validator = partial(type_validator, cls=float)


def validate(template: List[List[Any]], candidate: List[List[Any]]) -> bool:
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
                    return False

            current_column_index += 1
        current_row_index += 1
    return True

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
    with open('/Users/cthoyt/dev/income2019/tests/repeat_template.tsv') as _file:
        for x in parse_template(parse_tsv(_file)):
            print(x)
