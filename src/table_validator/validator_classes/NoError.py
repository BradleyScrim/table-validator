# -*- coding: utf-8 -*-

from .SheetError import SheetError

class NoError(SheetError):
    def __init__(self,row,column,value):
        super().__init__(row,column,value)

    def message(self):
        return "Everything fine at %d, %d: %s" %(self.row,self.column,self.value)
