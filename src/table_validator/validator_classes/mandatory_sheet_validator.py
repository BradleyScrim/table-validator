#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validator for 'not null'-fields
"""

from .sheet_validator import SheetError, SheetValidator

class MandatorySheetError(SheetError):

    # REM uses __init__() from LocationProvider
    
    def get_message(self):
        return "cell cannot be empty"

class MandatorySheetValidator(SheetValidator):

    # REM uses __init__() from LocationProvider

    def validate(self,value):
        if(value):
            return True,None
        else:
            return False,MandatorySheetError(self.row,self.column,value)
