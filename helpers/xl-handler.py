'''
XLHandler:
---------------------------------------------------------
handles any excel work using the xlsxwriter module
---------------------------------------------------------
'''

import xlsxwriter

class XLHandler:
    
     '''
    Create Column
    -------------------------
    
    '''
    def CreateCol(self, title, dataset):
        # HACK UNDONE