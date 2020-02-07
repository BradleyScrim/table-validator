#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validator for exact matches
"""

from .sheet_validator import SheetError, SheetValidator
import re

class RegexSheetError(SheetError):

    def __init__(self, row:int, column:int, actual_value:str, check_string:str):
        super().__init__(row, column, actual_value)
        self.__check_string=check_string

    def get_message(self):
        return "value '%s' should match '%s'" %(self.actual_value,self.__check_string)

class RegexSheetValidator(SheetValidator):

    def __init__(self,row:int,column:int,check_string:str):
        super().__init__(row, column)
        self.__check_string=check_string

    @property
    def check_string(self):
        return self.__check_string

    def validate(self,value):
        print(self.__check_string)
        print(value)
        print("---")
        m = re.fullmatch(self.__check_string,value)

        if(m != None):
            return True,None
        else:
            return False,RegexSheetError(self.row, self.column, value, self.__check_string)
