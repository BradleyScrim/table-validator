# -*- coding: utf-8 -*-


class TypeSheetValidator(SheetValidator):
    def __init__(self,row,column,cls):
        super(self,row,column)
        self.cls = cls

    def validate(self,value):
        try:
            self.cls(value)
        except ValueError:
            return False,ValidationErrorObject(row,column,"Wrong data type. Expected:", cls)
        else:
            return True,NoError(row,colum);
