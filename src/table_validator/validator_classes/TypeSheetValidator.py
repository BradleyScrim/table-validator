# -*- coding: utf-8 -*-

from .SheetValidator import SheetValidator
from .TypeSheetError import TypeSheetError
from .NoError import NoError

class TypeSheetValidator(SheetValidator):
    def __init__(self,row,column,cls):
        super().__init__(row,column)
        self.cls = cls

    def validate(self,value):
        try:
            self.cls(value)
        except ValueError:
            return False,TypeSheetError(self.row,self.column,value,self.cls)
        else:
            return True,NoError(self.row,self.column,value);
