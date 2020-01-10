#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validator for chemical compounds using the external java tool CompoundParser.jar
"""

import subprocess
from .sheet_validator import SheetError, SheetValidator

class SmartChemicalCompoundSheetError(SheetError):

    def __init__(self, row:int, column:int, actual_value:str, output:str ,error_message:str):
        super().__init__(row, column, actual_value)
        self.__output=output
        self.__error_message=error_message
    
    def get_message(self):
        return "Compound Validation failed with output '%s' and error message %s" %(self.__output,self.__error_message)

class SmartChemicalCompoundSheetValidator(SheetValidator):

    # REM uses __init__() from LocationProvider

    def validate(self,value):
        # get the cell value into input json format
        args=["{\"value\":\"" + value + "\"}"]
        # run external java program
        p = subprocess.Popen('java -jar CompoundParser/CompoundParser.jar '+' '.join(args), stdout=subprocess.PIPE, shell=True)
        # get output and return code
        output, err = p.communicate()
        p_return_code = p.wait()
        # validation
        if(p_return_code == 0):
            return True,None
        else:
            return False,SmartChemicalCompoundSheetError(self.row, self.column, value, output, err)
