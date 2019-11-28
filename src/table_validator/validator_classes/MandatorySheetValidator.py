# -*- coding: utf-8 -*-

from .SheetValidator import SheetValidator
from .MandatorySheetError import MandatorySheetError

class MandatorySheetValidator(SheetValidator):
# TODO a non-null value must be present
    def __init__(self,row,column):
        super().__init__(row,column)

    def validate(self,value):
        if(value):
            return True,None
        else:
            return False,MandatorySheetError(self.row,self.column,self.value)
