#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validator for exact matches
"""

from .sheet_validator import SheetError, SheetValidator
from .regex_sheet_validator import RegexSheetError, RegexSheetValidator

class ChebiSheetError(SheetError):

    def __init__(self, row:int, column:int, actual_value:str):
        super().__init__(row, column, actual_value)

    def get_message(self):
        return "value '%s' is not a valid CHEBI ID" %(self.actual_value)

class ChebiSheetValidator(RegexSheetValidator):

    def __init__(self,row:int,column:int):
        super().__init__(row, column,"CHEBI:[0-9]+")

    @property
    def check_string(self):
        return self.__check_string

    def validate(self,value):
        # TODO issue#5 possibly strip of trailing whitespace
        return(super().validate(value))
        if(False):
            return True,None
        else:
            return False,ChebiSheetError(self.row, self.column, value)
