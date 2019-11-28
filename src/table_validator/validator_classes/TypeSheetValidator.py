# -*- coding: utf-8 -*-

import SheetValidator, TypeSheetError, NoError

class TypeSheetValidator(SheetValidator):
    def __init__(self,row,column,cls):
        super(self,row,column)
        self.cls = cls

    def validate(self,value):
        try:
            self.cls(value)
        except ValueError:
            return False,TypeSheetError(self.row,self.column,"Wrong data type. Expected:", self.cls)
        else:
            return True,NoError(self.row,self.column);
