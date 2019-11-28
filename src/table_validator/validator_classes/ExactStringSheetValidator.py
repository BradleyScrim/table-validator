# -*- coding: utf-8 -*-

from .SheetValidator import SheetValidator
from .ExactStringSheetError import ExactStringSheetError

class ExactStringSheetValidator(SheetValidator):
# TODO a non-null value must be present
    def __init__(self,row,column,inString):
        super().__init__(row,column)
        self._string = inString;

    def validate(self,value):
        # TODO possibly strip of trailing whitespace
        if(value == self._string):
            return True,None
        else:
            return False,ExactStringSheetError(self.row,self.column,value,self._string)
