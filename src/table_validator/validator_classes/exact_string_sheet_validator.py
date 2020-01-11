#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validator for exact matches
"""

from .sheet_validator import SheetError, SheetValidator

class ExactStringSheetError(SheetError):

    def __init__(self, row:int, column:int, actual_value:str, check_string:str):
        super().__init__(row, column, actual_value)
        self.__check_string=check_string
    
    def get_message(self):
        return "value should be '%s'" %(self.__check_string)

class ExactStringSheetValidator(SheetValidator):

    def __init__(self,row:int,column:int,check_string:str):
        super().__init__(row, column)
        self.__check_string=check_string

    @property
    def check_string(self):
        return self.__check_string

    def validate(self,value):
        # TODO issue#5 possibly strip of trailing whitespace
        if(value == self.__check_string):
            return True,None
        else:
            return False,ExactStringSheetError(self.row, self.column, value, self.__check_string)
