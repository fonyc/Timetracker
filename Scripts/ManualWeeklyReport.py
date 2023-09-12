from datetime import datetime, timedelta
from ReportGenerator import GenerateWeeklyReport
if __name__ == "__main__":
    now = datetime.now()
    fiveDaysBefore = now - timedelta(days=5)
    fiveDays_str = datetime.strftime(fiveDaysBefore, "%d/%m/%Y")
    now_str = datetime.strftime(now, "%d/%m/%Y")
    print("\n")
    print("--- Press 1) to generate custom Weekly date report --- \n")
    print("--- Press 2) to generate today's report (from: "+ fiveDays_str + " to " + now_str + ") --- \n")

    choice = input()
    print("Option " + choice +  " selected \n")

    if(int(choice) == 1):
        date_string = input("Input the date you want to create the report in the shape of DD-MM-YYYY\n")
        GenerateWeeklyReport(date_string)

    elif(int(choice) == 2):
        GenerateWeeklyReport()
    else:
        print("Choice "+ choice + "is not a valid option")
