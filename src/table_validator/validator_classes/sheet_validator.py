#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
this file contains the basic construct for validation purpose

- LocationProvider - base class just providing everything for the row and column
- SheetValidator - base class for the validation logic
- SheetError - base class for the validator error object
"""
from abc import ABC,abstractclassmethod

class LocationProvider(ABC):
    """this abstract super class only provides the row/column base"""

    def __init__(self,row:int,column:int):
        self.__row = row
        self.__column = column

    @property
    def row(self) -> int:
        return self.__row
    
    @property
    def col(self) -> int:
        return self.__column
    @property
    def column(self) -> int:
        return self.col

    def get_location(self) -> (int,int):
        return self.__row,self.__column

class SheetError(LocationProvider):
    """the abstract super class of all validation errors
    
    initiate with row, column and the actual value of the defective cell
    no states: find error → create error object → don't change it anymore
    """

    def __init__(self, row:int, column:int, actual_value:str):
        super().__init__(row, column)
        self.__actual_value=actual_value

    @property
    def actual_value(self) -> int:
        return self.__actual_value

    @abstractclassmethod
    def get_message(self) -> str:
        """this method returns the error-specific message string"""

    def get_formatted_location(self):
        """returns a formatted version of the errors location, i.e. '5, 42'"""
        return "%d, %d" %(self.row, self.column)

    def get_formatted_full_error_message(self):
        """returns the location and message, pre-formatted for terminal output""" 
        return "%s [%s]: %s" %(self.get_location(), self.__actual_value, self.get_message())

class SheetValidator(LocationProvider):
    """the abstract super class of all validators
    
    initiate with row and column in case of an error
    no states: create validator object for current cell → call validate method
    """

    # REM uses __init__() from LocationProvider

    @abstractclassmethod
    def validate(self,value) -> (bool,SheetError):
        """this method does the actual validation and
        
        returns true,None if passed and false false,SheerError on validation error
        """
