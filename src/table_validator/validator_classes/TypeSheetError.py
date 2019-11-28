# -*- coding: utf-8 -*-

from .SheetError import SheetError

class TypeSheetError(SheetError):
    def __init__(self,row,column,value,cls):
        super().__init__(row,column,value)
        self.cls = cls

    def message(self):
        return "%d, %d: String '%s' is not of type %s" %(self.row,self.column,self.value,self.cls)
