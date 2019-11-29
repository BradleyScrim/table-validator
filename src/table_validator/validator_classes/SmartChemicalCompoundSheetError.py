# -*- coding: utf-8 -*-

from .SheetError import SheetError

class SmartChemicalCompoundSheetError(SheetError):
    def __init__(self,row,column,value,output,err):
        super(self,row,column,value)
        self.output=str(output)
        self.err=str(err)

    def message(self):
        return "%d, %d: %s Compund Validation failed with output %s and error message %s" %(self.row,self.column,self.value,self.output,self.err)
