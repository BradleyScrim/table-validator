# -*- coding: utf-8 -*-

import subprocess
from .SheetValidator import SheetValidator
from .SmartChemicalCompoundSheetError import SmartChemicalCompoundSheetError

class SmartChemicalCompoundSheetValidator(SheetValidator):
    def __init__(self,row,column):
        super().__init__(row,column)

    # checks that something is a compound
    def validate(self,value):
        # get the cell value into input json format
        args=["{\"value\":\"" + value + "\"}"]
        # run external java program
        p = subprocess.Popen('java -jar MockPig.jar '+' '.join(args), stdout=subprocess.PIPE, shell=True)
        # get output and return code
        output, err = p.communicate()
        p_return_code = p.wait()
        # validation
        if(p_return_code == 0):
            return True,None
        else:
            return False,SmartChemicalCompoundSheetError(self.row,self.column,self.value, output, err)
