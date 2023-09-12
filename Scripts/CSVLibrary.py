import csv
import os
import pandas as pd
from enum import Enum
from datetime import *

# Variables #
script_dir = "/home/pi/Desktop/Timetracker/"
script_dir_windows = "C:/Users/fonyc/Desktop/Timetracker/"
class Events(Enum):
    NONE = 1
    ENTRY = 2
    DEPARTURE = 3
    TOTALHOURS = 4

# Functions #
def IsPathFileValid(csv_path):
	return os.path.isfile(csv_path)

def GetAbsolutePathToDatabaseFile():
    return os.path.join(script_dir_windows, 'Database', 'Employees.csv')

#Date must be given as string
def GetAbsolutePathToRawSheetsFile(date):
    newRawSheetName = "RawTimeSheet_" + date + ".csv"
    return os.path.join(script_dir_windows, 'RawSheets', newRawSheetName)

#date must be given as string
def GetAbsolutePathToReportFile(date):
    newReportName = "Report_" + date + ".csv"
    return os.path.join(script_dir_windows, 'Reports/Daily', newReportName)

def GetAbsolutePathToWeeklyReportFile(firstDate, lastDate):
	newReportName = "WeeklyReport_" + firstDate + "_" + lastDate + ".csv"
	return os.path.join(script_dir_windows, 'Reports/Weekly', newReportName)
	
def GetEmployeeInDB(filepath, id):
	convertedId = "%d" % id
	with open(filepath, 'r') as csvfile:
		csvreader = csv.reader(csvfile)

		for row in csvreader:
			if row[0] == convertedId:
				return row[0], row[1]
	return -1, ""

#Creates a new file and adds the firstEntry
def CreateNewRawSheet(csv_path):
	df = pd.DataFrame(columns=['Id', 'Name', 'Time'])
	df.to_csv(csv_path, index=False)

def AddNewEntry(csv_path, Id, Name, Time):
	df = pd.read_csv(csv_path)
	df.loc[len(df.index)] = [Id, Name, Time]
	df.to_csv(csv_path, index=False)

def CreateFinalReport(finalReportPath):
	df = pd.DataFrame(columns=['Id', 'Name', 'Event','Time','Total'])
	df.to_csv(finalReportPath, index=False)

#Return an array of the Ids that exist in the RawDataSheet, meaning how much people whent to work today
def GetWorkingEmployees(date):
	df = pd.read_csv(GetAbsolutePathToRawSheetsFile(date))
	ids = df['Id'].unique()
	ids.sort()
	return ids