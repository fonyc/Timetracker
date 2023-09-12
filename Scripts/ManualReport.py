from ReportGenerator import GenerateReport
if __name__ == "__main__":
    print("\n")
    print("--- Press 1) to generate custom date report --- \n")
    print("--- Press 2) to generate today's report --- \n")

    choice = input()
    print("Option " + choice +  " selected \n")

    if(int(choice) == 1):
        date_string = input("Input the date you want to create the report in the shape of DD-MM-YYYY\n")
        GenerateReport(date_string)

    elif(int(choice) == 2):
        GenerateReport()
        
    else:
        print("Choice "+ choice + "is not a valid option")
