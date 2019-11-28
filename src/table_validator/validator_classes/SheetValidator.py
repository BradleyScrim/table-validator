# -*- coding: utf-8 -*-

import SheetError

class SheetValidator:
    
    def __init__(self,row,column):
            self.row = row
            self.column = column
    # the location this is responsible for in the sheet
    def getLocation(self):
        return self.row,self.column

    # this does the actual validation
    # this empty validator always succeeds
    def validate(self,value):
        return True,SheetError(self.row,self.column,self.value)
