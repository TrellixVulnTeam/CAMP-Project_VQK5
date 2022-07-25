import xlwings as xw
import json
import os
from datetime import datetime
import confiq 


#Model File
MODEL_FILE = confiq.DIR_PATH + '/models/model-file-camp-sankey.xlsx'
MODEL_SHEET = 'app'
INPUT_FIELDS_RANGE = 'A4:I12' 
INPUTS_START_CELL = 'G5' #Start of Highlighted Fields
#OUTPUT_FIELDS_RANGE = 'A56:E83'
#model-file-camp-sankey
#model-file-khcam


#-------------------------------------------
#       Public Methods
#-------------------------------------------

def modelFile():
    # app = xw.App(visible=False)
    wb = xw.Book(MODEL_FILE)
    ws = wb.sheets[MODEL_SHEET]
    print(xw.apps)
    return ws

def getInputsFields(ws):
    # getInputsFields
    data = ws.range(INPUT_FIELDS_RANGE).value
    return toDict(data)

def setInputsCell(ws, inputsList):
    # setInputValues by cell
    for i in inputsList:
        ws.range(i['id']).options(transpose=False).value = i['value']

def setInputs(ws, inputsList):
    # setInputValues by range
    ws.range(INPUTS_START_CELL).options(transpose=True).value = inputsList #changed it from True

# def getOutput(ws):
#     # getOutputValues
#     data = ws.range(OUTPUT_FIELDS_RANGE).value
#     return toDict(data)


app_dir= confiq.DIR_PATH 

command = 'python3 SankeyScript.py'


def generateOutput():
    print(command)
    os.popen(command)
    


#command = 'cd {} python3 SankeyScript.py"'.format(app_dir)















#-------------------------------------------
#       Private Methods
#-------------------------------------------
def toDict(data):
    """
        this restructure data
    """
    result=[]
    for row in data[1:]:
        result.append(dict(zip(data[0], row)))
    return result

    

    #exec(open("SankeyScript.py").read())
    #subprocess.call("SankeyScript.py", shell=True)
    #os.system('SankeyScript.py')