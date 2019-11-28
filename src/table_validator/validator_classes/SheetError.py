# -*- coding: utf-8 -*-

class SheetError:
    def __init__(self,row,column,value):
        self.row = row;
        self.column = column
        self.value = value

    def message(self):
        return "%d, %d: %s" %(row,column,value)
