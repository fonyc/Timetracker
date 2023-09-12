from CSVLibrary import *
from datetime import datetime, timedelta
from CSVLibrary import Events

def CalculateTotalHours(data_list):
    if len(data_list) % 2 != 0:
        return -1
    else:   
        total_time = timedelta()
        time_objs = [datetime.strptime(t, '%H:%M:%S').time() for t in data_list]
        sortedTimes = sorted(time_objs)

        for x in range (0,len(sortedTimes)-1,2):
            dt1 = datetime.combine(datetime.today(), sortedTimes[x])
            dt2 = datetime.combine(datetime.today(), sortedTimes[x+1]) 
            time_diff = dt2 - dt1
            total_time += time_diff
    return  ConvertDeltaIntoString(total_time)

'''Given a deltatime type, convert it into a HH:MM:SS string time'''
def ConvertDeltaIntoString(duration):
    return "{:02d}:{:02d}:{:02d}".format(duration.seconds // 3600, (duration.seconds % 3600) // 60, duration.seconds % 60)

#Recieves date as string input and generates the report given that date
def GenerateReport(date = datetime.now().strftime("%d-%m-%Y")):
    # Check if the rawSheet exists for the requested date
    rawSheetFilePath = GetAbsolutePathToRawSheetsFile(date)
    if(IsPathFileValid(rawSheetFilePath)):
        peopleIds = GetWorkingEmployees(date)
        CreateFinalReport(GetAbsolutePathToReportFile(date))
        dfRaw = pd.read_csv(rawSheetFilePath)
        dfReport = pd.read_csv(GetAbsolutePathToReportFile(date))

        my_dict = []
        for employeeId in peopleIds:
            index = 0
            lastName = any
            temp_dict = []
            for row in dfRaw.iterrows():
                if row[1]['Id'] == employeeId:
                    if index % 2 == 0:
                        #Add entry row to dict
                        my_dict.append({'Id': employeeId, 'Name': row[1]['Name'], 'Event': Events.ENTRY.name ,'Time': row[1]['Time']})
                        temp_dict.append({'Id': employeeId, 'Name': row[1]['Name'], 'Event': Events.ENTRY.name ,'Time': row[1]['Time']})
                    else:
                        #Add Departure row to dict
                        my_dict.append({'Id': employeeId, 'Name': row[1]['Name'], 'Event': Events.DEPARTURE.name ,'Time': row[1]['Time']})
                        temp_dict.append({'Id': employeeId, 'Name': row[1]['Name'], 'Event': Events.ENTRY.name ,'Time': row[1]['Time']})
                    index += 1
                    lastName = row[1]['Name']

            dfReport = pd.DataFrame(temp_dict)
            time_series = dfReport.loc[:, 'Time']

            totalHours = CalculateTotalHours(time_series)
            my_dict.append({'Id': employeeId, 'Name': lastName, 'Event': Events.TOTALHOURS.name , 'Total': totalHours})

        #Add the dictionary to the final Report
        dfReport = pd.DataFrame(my_dict)

        # Write the DataFrame to a CSV file
        dfReport.to_csv(GetAbsolutePathToReportFile(date), index=False)

        #Save it into the shared drive
        #report_path = "/home/pi/mnt/stickypc/Reports/" + "Report_" + date + ".csv"
        #dfReport.to_csv(report_path, index=False)

#Generate, given a string date, a weekly report from 5 reports (can be configured to take more reports)
def GenerateWeeklyReport(date = datetime.now().strftime("%d-%m-%Y")):
    weeklyReportNames = GetLastNReportNames(date, 5)
    firstDate = GetLastReportDate(date, 5)
    weekHoursDict = []

    for x in range (0, len(weeklyReportNames)):
        df = pd.read_csv(weeklyReportNames[x])
        #Remove "-1" fields that means taht someone had inconsistent data report
        is_total_not_minus_1 = (df['Total'] != -1)
        dfReport = df[is_total_not_minus_1]
        for report_row in dfReport.iterrows():
            if(report_row[1]['Event'] == Events.TOTALHOURS.name and not pd.isnull(report_row[1]['Total'])):
                isNewEntry = True
                for entry in weekHoursDict:
                    if entry['Id'] == report_row[1]['Id']:
                        isNewEntry = False
                        entry['Total_Hours'] = int(entry['Total_Hours']) + GetHoursFromDate(report_row[1]['Total'])
                        entry['Total_Minutes'] = int(entry['Total_Minutes']) + GetMinutesFromDate(report_row[1]['Total'])
                        if(int(entry['Total_Minutes']) > 60):
                            minutes = int(entry['Total_Minutes'])
                                
                            extraHours, remainder = divmod(minutes, 60)
                            entry['Total_Hours'] += extraHours
                            entry['Total_Minutes'] = remainder
                        break
                #First time the ID appears. Add new entry
                if(isNewEntry == True):       
                    newEntry = {'Id': report_row[1]['Id'], 
                                'Name': report_row[1]['Name'], 
                                'Total_Hours': GetHoursFromDate(report_row[1]['Total']), 
                                'Total_Minutes': GetMinutesFromDate(report_row[1]['Total'])}
                    weekHoursDict.append(newEntry)
    
    dfReport = pd.DataFrame(weekHoursDict)
    # Write the DataFrame to a CSV file
    dfReport.to_csv(GetAbsolutePathToWeeklyReportFile(firstDate, date), index=False)

def GetHoursFromDate(time):
    time = str(time)
    timeObject = datetime.strptime(time, "%H:%M:%S")
    return int(timeObject.hour)

def GetMinutesFromDate(time):
    time = str(time)
    timeObject = datetime.strptime(time, "%H:%M:%S")
    return int(timeObject.minute)

'''Given an initial string date, get the N report full path names and backwards'''
def GetLastNReportNames(date, n):
    reportNames = []
    for x in range(0, n):
        objectDate = datetime.strptime(date, "%d-%m-%Y")
        previousDate = objectDate - timedelta(days=x)
        previousDateString = datetime.strftime(previousDate, "%d-%m-%Y")
        reportName = GetAbsolutePathToReportFile(previousDateString)
        if(IsPathFileValid(reportName)):
            reportNames.append(reportName)
    return reportNames

#Given a date and a number returns the  
def GetLastReportDate(date, n):
    objectDate = datetime.strptime(date, "%d-%m-%Y")
    previousDate = objectDate - timedelta(days=n-1)
    return datetime.strftime(previousDate, "%d-%m-%Y")