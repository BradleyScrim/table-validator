# -*- coding: utf-8 -*-

from .TypeSheetValidator import TypeSheetValidator

class IntSheetValidator(TypeSheetValidator):
    def __init__(self,row,column):
        super().__init__(row,column,float)

# the validate method gets inherited