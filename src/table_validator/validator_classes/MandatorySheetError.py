# -*- coding: utf-8 -*-

import SheetError

class MandatorySheetError(SheetError):
    def __init__(self,row,column,value,cls):
        super(self,row,column,value)
        self.cls = cls

    def message(self):
        return "%d, %d: %s should have been of type %s" %(self.row,self.column,self.value,self.cls)
