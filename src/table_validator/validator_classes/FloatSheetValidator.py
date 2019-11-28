# -*- coding: utf-8 -*-

from .TypeSheetValidator import TypeSheetValidator

class FloatSheetValidator(TypeSheetValidator):
    def __init__(self,row,column):
        super().__init__(row,column,float)

# the validate method gets inherited
