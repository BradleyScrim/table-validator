# -*- coding: utf-8 -*-
from .SheetError import SheetError

class ExactStringSheetError(SheetError):
    def __init__(self,row,column,value,_string):
        super().__init__(row,column,value)
        self._string = _string

    def message(self):
        return "%d, %d: %s should be %s" %(self.row,self.column,self.value,self._string)
