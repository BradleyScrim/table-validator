# -*- coding: utf-8 -*-

class MandatorySheetValidator(SheetValidator):
# TODO a non-null value must be present
    def __init__(self,row,column):
        super(self,row,column)

    def validate(self):
        return True,SheetError(row,column,value)
