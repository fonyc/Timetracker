from CSVLibrary import (GetEmployeeInDB, IsPathFileValid, GetAbsolutePathToDatabaseFile, 
                        GetAbsolutePathToRawSheetsFile, CreateNewRawSheet, AddNewEntry)
from datetime import datetime
from Buzzer import NegativeSoundFeedback, PositiveSoundFeedback
from LCDLibrary import PrintLCDEvent, CleanLCD

# --- CODE --- #
def InputTime(id):
    Employee = GetEmployeeInDB(GetAbsolutePathToDatabaseFile(), id)
    #The user is a valid Stickylock employee
    if(Employee[0] != -1):
        now = datetime.now()

        #Conform the file "Timesheet_Date"
        csv_path = GetAbsolutePathToRawSheetsFile(now.strftime("%d-%m-%Y"))
        
        if(IsPathFileValid(csv_path) == False):
            CreateNewRawSheet(csv_path)

        AddNewEntry(csv_path, Employee[0], Employee[1], now.strftime("%H:%M:%S"))  
        PositiveSoundFeedback()
        #Print LCD Feedback
        LCDFormatedDate = "    " + now.strftime("%H:%M:%S")+ "    "
        return Employee[1],LCDFormatedDate
    else:
        NegativeSoundFeedback()
        return "  No user found ",""
