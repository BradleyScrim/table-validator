#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validators for type checks

this file contains the
- abstract base TypeSheetValidator implementing the check for a type
- concrete type validators 
"""

from .sheet_validator import SheetError, SheetValidator

class TypeSheetError(SheetError):

    def __init__(self, row:int, column:int, actual_value:str, check_class:type):
        super().__init__(row, column, actual_value)
        self.__check_class=check_class
    
    def get_message(self):
        return "string is not of type '%s'" %(self.__check_class)

class TypeSheetValidator(SheetValidator):
    """tries to convert the content of a cell to the defined class"""

    def __init__(self, row:int, column:int, check_class:type):
        super().__init__(row, column)
        self.__check_class=check_class

    @property
    def check_class(self):
        return self.__check_class

    def validate(self,value):
        try:
            self.__check_class(value)
        except ValueError:
            return False,TypeSheetError(self.row, self.column, value, self.__check_class)
        else:
            return True,None

class IntTypeSheetValidator(TypeSheetValidator):
    def __init__(self,row,column):
        super().__init__(row,column,int)

class FloatTypeSheetValidator(TypeSheetValidator):
    def __init__(self,row,column):
        super().__init__(row,column,float)
