# -*- coding: utf-8 -*-

"""Validator classes for ``table_validator``."""

from typing import TextIO, Union

from .api import parse_tsv, validate

__all__ = [
    'TemplateValidator',
]

class TemplateValidator:
    """ Class validating a file based on a template"""
    def __init__(self, template):

        print("were here");
        print(self);
        print(template);

        if isinstance(template, str):  # is a path
            with open(template) as file:
                print("works?")
                self.template = parse_tsv(file)
        elif isinstance(template, list):  # is pre-parsed
            print("works2?")
            self.template = template
        # FIXME: if true…
        elif True or isinstance(template, TextIO):# always.... does it break?
            print("works3?")
            self.template = parse_tsv(template)
        print("self template");
        print(self.template);

    def validate(self, candidate: Union[list, TextIO]) -> bool:
        print("in validate:");
        print(self);
        if isinstance(candidate, list):
            return validate(self.template, candidate)
        return validate(self.template, parse_tsv(candidate))

    def __call__(self, candidate: Union[list, TextIO]) -> bool:
        return self.validate(candidate)
