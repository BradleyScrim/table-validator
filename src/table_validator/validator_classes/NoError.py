# -*- coding: utf-8 -*-

from .SheetError import SheetError

class NoError(SheetError):
    def __init__(self,row,column):
        super().__init__(row,column)

    def message(self):
        return "Everything fine at %d, %d: %s" %(row,column,value)
