# -*- coding: utf-8 -*-

class NoError:
    def __init__(self,row,column,value):
        self.row = row;
        self.column = column
        self.value = value

    def message(self):
        return "Everything fine at %d, %d: %s" %(self.row,self.column,self.value)
