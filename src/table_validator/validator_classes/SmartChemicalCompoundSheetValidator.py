# -*- coding: utf-8 -*-

from .SheetValidator import SheetValidator
from .SmartChemicalCompoundSheetError import SmartChemicalCompoundSheetError

class SmartChemicalCompoundSheetValidator(SheetValidator):
    def __init__(self,row,column):
        super().__init__(row,column)

    # TODO checks that something is a compound
    def validate(self,value):
        if(value):
            return True,None
        else:
            return False,SmartChemicalCompoundSheetError(self.row,self.column,self.value)
