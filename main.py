import csv
from Test import Test
from Record import Record
import re
from datetime import datetime, timedelta


#line = line.strip()


#===================================================medicalRecord===================================================
# initialize the dicteonry 
def creat_medical_record_list():
    
    record_dict.clear()
    
    fo = open("medicalRecords.txt", "r+") 
    list = fo.read().split("\n")
    fo.close()
    for i in list:
        # try for the whole loop
        try:
            if len(i.split(",")) != 5 and len(i.split(",")) != 6:
                continue
            PID = int(i.split(",")[0].split(": ")[0]) 
            test_symbol = i.split(",")[0].split(": ")[1]

        
            begin_time = i.split(", ")[1]
            result = float(i.split(", ")[2])
            unit = i.split(", ")[3]
        # Check if one of the three ( pending...... ) and do regular expression to accept [pP]ending 
            status = i.split(", ")[4]
            if re.match(r"[Cc]ompleted", status) is not None:
                completed_time = i.split(", ")[5]
            elif re.match(r"[rR]eviewed", status) is not None or re.match(r"[pP]ending", status) is not None:
                test = get_test(test_symbol)
                if is_more_than_current_date(begin_time, test)[0] == False:
                    status = "completed"
                    completed_time = str(is_more_than_current_date(begin_time, test)[1])
                  
            record = Record(test_symbol, begin_time, result, unit, status, completed_time)
        
        # record_list.append(record)
        
            if PID in record_dict:
                record_dict[PID].append(record)
            else:
                record_dict[PID] = [record]
        except Exception:
            continue

    for key, record in record_dict.items():
        for i in range(len(record) - 1, -1, -1):
            if is_availabe_test(record[i].get_name()) is not True:
                print("Test with that symbol", record[i].get_name(),  "does not exist\n")
                record.pop(i)
            
    newFile = ""
    
    for key, record in record_dict.items():
        for i in record:
            try:
                newFile += str(key) + ": " + do_record_dict_format(i) + "\n"
            except Exception:
                print("Not valid format")
                return

    newFile = newFile[0:len(newFile) - 1] # to handle the \n
    fo = open("medicalRecords.txt", "w")
    fo.write(newFile)
    fo.close()
      
# Update mediacl record for a patient and submit changes to file
def update_medical_record():
    fo = open("medicalRecords.txt", "r+")
    whole_file = fo.read()
    fo.close()
    
    line_list = whole_file.split("\n") #list contain all records
    patient_list = [] # list contain all patient's records
    # some exceptions
    try:
        PID = int(input("Enter patient ID\n"))
    except Exception:
        print("Not valid Patient id")
        return
    if len(str(PID)) != 7:
        print("Please enter 7 digits")
        return

    if PID not in record_dict:
        print("No patient with this ID")
        return
    
    for i in line_list:
        if i[0:7] == str(PID):
            patient_list.append(i)

    print("\nEnter which medical Record you want to update based on number\n")
    for i in range(len(patient_list)):
        print (str(i + 1) + " " + str(patient_list[i]))
    try:
        p_line_number = int(input(""))
    except Exception:
        print("Enter a numerical value")
        return
    
    if p_line_number > len(patient_list):
        print("Enter a valid line number")
        return

    print("Is that the line you want to edit ? \n" + str(PID) + ": " + do_record_dict_format(record_dict[PID][p_line_number - 1]), "\n1-Yes\n2-NO")
    try:
        choice = int(input(""))
    except Exception:
        print("Enter a numerical value")
        return
        
    if choice != 1:
        print("\nTry Again!")
        return

    test_symbol = record_dict[PID][p_line_number - 1].get_name() # get the test by its P.K
    record_dict[PID].pop(p_line_number - 1) # pop the patient record to add the new one (easier than just edit it)

    if is_availabe_test(test_symbol) is not True: # if the test exist
        print("Test with that symbol", test_symbol,  "not exist, here are the list of all test symbols, or yo can add a new test\n")
        for i in testsList:
            i.to_string()
            print("\n")
        return
    try:
        op = int(input("Do you want to use the current time ?\n1-Yes\n2-NO.\n")) # to simplifiez the usage of the current time
    except Exception:
        print("Enter a numericall value")
        return
        
    if op < 1 or op > 2:
        print("Not valid option")
        return
    
    begin_time = 0 
    if op == 1:
        begin_time = str(datetime.now()).split(":")[0] + ":" + str(datetime.now()).split(":")[1]
    elif op == 2:
        begin_time = input("Enter when the test begain, Format: YYYY-MM-DD HH:MM\n")
        
    test = get_test(test_symbol)
    if is_more_than_current_date(begin_time, test) == None: # just to use the try catch inside
        return
    try:
        result = float(input("Enter the result\n"))
    except Exception:
        print("Enter a numerical result ): ")
        return

    unit = get_test(test_symbol).get_unit() # get the unit
    
    status = ""
    completed_time = ""

    if is_more_than_current_date(begin_time, test)[0] == False: # if not so it's either pending or reviewed
        print("The status set to be completed")
        status = "completed"
        completed_time = str(is_more_than_current_date(begin_time, test)[1])
    else:
        status_choice = int(input("Enter the test status,\n1- pending,\n2- reviewed\n"))
        if status_choice == 1:
            status = "pending"
        elif status_choice == 2:
            status = "reviewed"

    try:
        record = Record(test_symbol, begin_time, result, unit, status, completed_time)
    except Exception:
        print("Enter a valid date")
        return
    
    record_dict[PID].append(record) #append the record
    
    newFile = ""
    
    for key, record in record_dict.items():
        for i in record:
            try:
                newFile += str(key) + ": " + do_record_dict_format(i) + "\n"
            except Exception:
                print("Not valid format")
                return

    newFile = newFile[0:len(newFile) - 1] # Delete the last "\n"
    fo = open("medicalRecords.txt", "w")
    fo.write(newFile)
    fo.close()

# function to add new medical record to a specific patient
def add_new_medical_record():

    print("Enter the medical test according to the conventions\nfor more you can read test_conventions.txt file")
    try:
        PID = int(input("Enter the patient ID\n"))
    except Exception:
        print("Not valid value")
        return
    if len(str(PID)) != 7:
        print("Please enter 7 digits")
        return

    test_symbol = input("Enter the test symbol\n")
    if is_availabe_test(test_symbol) is not True:
        print("Test with that symbol", test_symbol,  "not exist, here are the list of all test symbols, or yo can add a new test\n")
        for i in testsList:
            i.to_string()
            print("\n")
        return
    test = get_test(test_symbol)
    try:
        op = int(input("Do you want to use the current time ?\n1-Yes\n2-NO.\n"))
    except Exception:
        print("Enter a numericall value")
        return
        
    if op < 1 or op > 2:
        print("Not valid option")
        return
    
    begin_time = 0 
    if op == 1:
        begin_time = str(datetime.now()).split(":")[0] + ":" + str(datetime.now()).split(":")[1]
    elif op == 2:
        begin_time = input("Enter when the test begain, Format: YYYY-MM-DD HH:MM\n")
        
    if is_more_than_current_date(begin_time, test) == None:
        return
    try:
        result = float(input("Enter the result\n"))
    except Exception:
        print("Enter a numerical result ): ")
        return
    unit = get_test(test_symbol).get_unit()
    # Make Sure ;
    
    status = ""
    completed_time = ""

    if is_more_than_current_date(begin_time, test)[0] == False:
        print("The status set to be completed")
        status = "completed"
        completed_time = str(is_more_than_current_date(begin_time, test)[1])
    else:
        try:
            status_choice = int(input("Enter the test status,\n1- pending,\n2- reviewed\n"))
        except:
            print("Enter a numerical Value ):")
        if status_choice == 1:
            status = "pending"
        elif status_choice == 2:
            status = "reviewed"
        else:
            print("Enter a valid option ):")
            return
    try:
        record = Record(test_symbol, begin_time, result, unit, status, completed_time)
    except Exception:
        print("Enter a valid begin time")
        return
        
    record_list.append(record)

    if PID in record_dict:
        record_dict[PID].append(record)
    else:
        record_dict[PID] = []
        record_dict[PID].append(record)

    try:
        fo = open("medicalRecords.txt", "r+")
    except Exception:
        print("File do not exist")
        return

    fo.read() # to point to the end of the file ( idk i just figuered i can use a insted of r+ ): )
    fo.write("\n" + str(PID) + ": " + do_record_dict_format(record))
    fo.close()

# to remove any out dated
def delete_out_dated_records():
    for key, record in record_dict.items():
        for i in range(len(record) - 1, -1, -1):
            if record[i].get_status() == "completed" and is_out_dated(record[i].get_completed_date()):
                print("h")
                record.pop(i)
            elif is_availabe_test(record[i].get_name()) is not True:
                print("Test with that symbol", record[i].get_name(),  "not exist, here are the list of all test symbols, or yo can add a new test\n")
                record.pop(i)
                for i in testsList:
                    i.to_string()
                    print("\n")
            
    newFile = ""
    
    for key, record in record_dict.items():
        for i in record:
            try:
                newFile += str(key) + ": " + do_record_dict_format(i) + "\n"
            except Exception:
                print("Not valid format")
                return

    newFile = newFile[0:len(newFile) - 1] # to handle the \n
    fo = open("medicalRecords.txt", "w")
    fo.write(newFile)
    fo.close()
    
   
# if is more than a year
def is_out_dated(record_date):
    try:

        year = int(record_date.split("-")[0])
        month = int(record_date.split("-")[1])
        day = int(record_date.split("-")[2].split(" ")[0])
        hour = int(record_date.split(" ")[1].split(":")[0])
        minute = int(record_date.split(" ")[1].split(":")[1])
        record_date = datetime(year, month, day, hour, minute, 0)

    except Exception:
        print("Enter a valid date")
        return None
    return (record_date < (datetime.now() - timedelta(days=365)))

# is it ?
def is_more_than_current_date(user_date, test_date):
    
    try:
        turn_around_date = timedelta(days=test_date.get_days(), seconds=0, microseconds=0, milliseconds=0, minutes=test_date.get_mins(), hours=test_date.get_hour(), weeks=0)

        year = int(user_date.split("-")[0])
        month = int(user_date.split("-")[1])
        day = int(user_date.split("-")[2].split(" ")[0])
        hour = int(user_date.split(" ")[1].split(":")[0])
        minute = int(user_date.split(" ")[1].split(":")[1])
        user_date = datetime(year, month, day, hour, minute, 0)

        compined_date = turn_around_date + user_date

    except Exception:
        print("Enter a valid date")
        return None
    
    if user_date > datetime.now():
        print("Congrats! you managed to go to the futre, You should be at NASA not some low budget medical clinic")
        return None

    return [compined_date > datetime.now(), compined_date]

# convert from the format of a list to csv file ( with spaces )
# without accessing the PID 
def do_record_dict_format(record):
    first_field = str(record.get_name()) + ","
    second_field = str(record.get_begin_date()) + ","
    third_field = str(record.get_result()) + ","
    forth_field = str(record.get_unit()) + ","
    fifth_field = str(record.get_status())
    sixth_field = ""
    if re.match(r"[Cc]ompleted", record.get_status()) is not None:
        sixth_field = str(record.get_completed_date())
        fifth_field += ","
        return first_field + " " + second_field + " " + third_field + " " + forth_field + " "  + fifth_field + " " + sixth_field
    return first_field + " " + second_field + " " + third_field + " " + forth_field + " "  + fifth_field

#===================================================medicalRecord===================================================


#===================================================medicalTest===================================================

# test that file like you edeted the others, but check the comments
def update_medical_test():
    fo = open("medicalTests.txt", "r+")
    whole_file = fo.read()
    print(whole_file)
    try:
        line_number = int(input("\nEnter which medical Test you want to update based on number\n"))
    except Exception:
        print("Just numbers")
        return
    fo.close()
    
    line_list = whole_file.split("\n")
    #Check if it's not 1 or 2
    print("Is that the line you want to edit ? \n", line_list[line_number - 1], "\n1-Yes\n2-NO")
    try:
        choice = int(input(""))
    except Exception:
        print("Enter a numerical value")
        return
        
    if choice != 1:
        print("\nTry Again!")
        return
    symbol = testsList[line_number - 1].get_symbol()
    line_list.pop(line_number - 1)
    testsList.pop(line_number - 1)
    
    for i in range(len(line_list)):
        j = i + 1
        line_list[i] = str(j) + ". " + line_list[i].split(". ")[1]
    
    newFile = ""
    for i in line_list:
        newFile += i + "\n"
    
    print("Enter the medical test according to the conventions\nfor more you can read test_conventions.txt file")
    name = input("Please enter the test name\n")
    if name.isalpha() == False and " " not in name and "-" not in name:
        print("Please enter the test name in alphabet (can contain alphabatic, -n and white spaces)\n")
        return

    try:
        minRange = float(input("Enter the minimum value, if none Enter \n"))
    except Exception:
        print("Enter a valid number")
        return
    try:
        maxRange = float(input("Enter the maximum value, if none Enter -1\n"))
    except Exception:
        print("Enter a number")
    unit = input("Enter the test unit\n")
    time = input("Enter the time required on that format DD-HH-MM\n")
    try:
        days = int(time.split("-")[0])
        hours = int(time.split("-")[1])
        mins = int(time.split("-")[2])
    except Exception:
        print("Enter a valid number")
        return
    
    test = Test(symbol, minRange, maxRange, unit, days, hours, mins)
    testsList.append(test)
    test_format = do_test_format(name, symbol, minRange, maxRange, unit, time, len(testsList))
    print(len(testsList))
    print(do_test_format(name, symbol, minRange, maxRange, unit, time, len(testsList)))
    fo = open("medicalTests.txt", "w")
    newFile += test_format
    fo.write(newFile)
    fo.close()

def add_new_medical_test():
    print("Please Enter the medical test according to the conventions\nfor more you can read test_conventions.txt file")
    name = input("Please enter the test name\n")
    if name.isalpha() == False and " " not in name and "-" not in name:
        print("Please enter the test name in alphabet (can contain alphabatic, -n and white spaces)\n")
        return
    symbol = input("Please enter the symbol\n")
    if symbol.isalpha() == False:
        print("Please enter the symbol in alphabet form (just alphabatic chars)\n")
        return
    if get_test(symbol) is not None:
        print("This symbol is already exist, enter another one")
        return
    try:
        minRange = int(input("Please enter the minimum value, if none please enter -1\n"))
    except Exception:
        print("Please enter a valid number")
        return
    try:
        maxRange = int(input("Please enter the maximum value, if none please enter -1\n"))
    except Exception:
        print("Please enter a valid number")
        return
    if minRange > maxRange:
        print("Min Range is more then max Range\n")
        return
    
    unit = input("Please enter the test unit\n")
    time = input("Please enter the time required on that format DD-HH-MM\n")
    if time.count("-") != 2:
        print("Please enter the date in general format DD-HH-MM,add (-) between date\n")
        return
    temptime = time.split("-")  # time[0]=day -- time[1]=hour -- time[2]=minute)
    day=temptime[0]
    hour=temptime[1]
    mins=temptime[2]
    if temptime[0].isdigit() == False or temptime[1].isdigit() == False or temptime[2].isdigit() == False:
        print("please enter the time using digit number [0-9]\n")
        return
    test = Test(symbol, minRange, maxRange, unit, day, hour, mins)
    testsList.append(test)
    test_format = do_test_format(name, symbol, minRange, maxRange, unit, time, len(testsList))
    fo = open("medicalTests.txt", "r+")
    fo.read()
    fo.write("\n" + test_format)
    fo.close()

# Conver from test class to csv file
def do_test_format(name, symbol, minRange, maxRange, unit, time, lenght):
    first_field = str(lenght) + ". Name: " + name + " (" + symbol + ");"
    second_field = ";"
    if minRange != -1 and maxRange != -1:
        second_field = "Range: > " + str(minRange) + ", < " + str(maxRange) + ";"
    elif maxRange == -1:
        second_field = "Range: > " + str(minRange) + ";"
    elif minRange == -1:
        second_field = "Range: < " + str(maxRange) + ";"
    third_field = "Unit: " + str(unit) + ", " + str(time)

    return first_field + " " + second_field + " " + third_field

# initialize the test list
def creatMedicalTestList():

    fo = open("medicalTests.txt", "r+")
    linesList = fo.read().split("\n")
    fo.close()
    for i in linesList:
        symbol = i.split(";")[0].split("(")[1].split(")")[0]
        minRange = float(getMinRange(i.split(";")[1]))
        maxRange = float(getMaxRange(i.split(";")[1]))
        if minRange > maxRange and maxRange != -1:
            temp = minRange
            minRange = maxRange
            maxRange = temp
            
        unit = i.split(";")[2].split(",")[0].split(": ")[1]
        time = i.split(";")[2].split(", ")[1]
        days = int(time.split("-")[0])
        hours = int(time.split("-")[1])
        mins = int(time.split("-")[2])
        test = Test(symbol, minRange, maxRange, unit, days, hours, mins)
        testsList.append(test) 

# get the min range from the csv we have
def getMinRange(range):
    range = str(range)
    if ">" in range and "<" in range:
        return(float(range.split(",")[0].split(">")[1]))
    elif ">" in range:
        return(float(range.split(">")[1]))
    elif "<" in range:
        return -1
    return -1

# get the max range from the csv we have
def getMaxRange(range):
    range = str(range)
        
    if ">" in range and "<" in range:
        return(float(range.split(",")[1].split("<")[1]))
    elif "<" in range:
        return(float(range.split("<")[1]))
    elif ">" in range:
        return -1
    return -1

# is it ?
def is_availabe_test(symbol):
        for i in testsList:
            if symbol == i.get_symbol():
                return True
        return False

# simple (:
def get_test(symbol):
        for i in testsList:
            if symbol == i.get_symbol():
                return i
        return None
#===================================================medicalTest===================================================


#==================================================CodeFunctions==================================================

def write_on_csv():

    with open('medicalRecords.csv', 'w', newline='') as file: # to remove the file then open it again
        pass

    # write the Attribuites
    with open('medicalRecords.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["PID_test", "begin_date", "result", "unit", "status", "complete_date"])

    # paste the dict
    for key, record in record_dict.items():
        for i in record:
            with open('medicalRecords.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([str(key) + ": " + str(i.get_name()), i.get_begin_date(), i.get_result(), i.get_unit(), i.get_status(), i.get_completed_date()])

    # get data from csv
def import_from_csv():
    rec_dict.clear()
    data = []
    with open("medicalRecords.csv", mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)

    for item in data:
        if item[0] == "PID_test":
            continue
        key = int(item[0][0:7])
        item[0] = item[0][9:]
        record = Record(*item)
        if key in rec_dict:
            rec_dict[key].append(record)
        else:
            rec_dict[key] = [record]


    # is in specific period for test formt (dd-hh-mm)
def is_in_period_test_format(date1, date2, record): 
    try:
        test = get_test(record.get_name())
        day = int(test.get_days())
        hour = int(test.get_hour())
        minute = int(test.get_mins())
        turn_around = timedelta(days=day, hours=hour, minutes=minute)
        
        day = int(date1.split("-")[0])
        hour = int(date1.split("-")[1])
        minute = int(date1.split("-")[2])
        date1 = timedelta(days=day, hours=hour, minutes=minute)
        
        day = int(date2.split("-")[0])
        hour = int(date2.split("-")[1])
        minute = int(date2.split("-")[2])
        date2 = timedelta(days=day, hours=hour, minutes=minute)
    except Exception:
        print("Not valid dates")
        return None

    return turn_around > date1 and turn_around < date2
    
# is in specific period for record formt (YYYY-MM-DD HH:MM)
def is_in_period(date1, date2, record):
    try:
        date = record.get_begin_date()
        year = int(date.split("-")[0])
        month = int(date.split("-")[1])
        day = int(date.split("-")[2].split(" ")[0])
        hour = int(date.split(" ")[1].split(":")[0])
        minute = int(date.split(" ")[1].split(":")[1])
        date = datetime(year, month, day, hour, minute, 0)
        
        year = int(date1.split("-")[0])
        month = int(date1.split("-")[1])
        day = int(date1.split("-")[2].split(" ")[0])
        hour = int(date1.split(" ")[1].split(":")[0])
        minute = int(date1.split(" ")[1].split(":")[1])
        date1 = datetime(year, month, day, hour, minute, 0)
        
        year = int(date2.split("-")[0])
        month = int(date2.split("-")[1])
        day = int(date2.split("-")[2].split(" ")[0])
        hour = int(date2.split(" ")[1].split(":")[0])
        minute = int(date2.split(" ")[1].split(":")[1])
        date2 = datetime(year, month, day, hour, minute, 0)

    except Exception:
        return None
    return date > date1 and date < date2

# is abnormal test (getting the test value manually)
def is_abnormal(record):
    test = get_test(record.get_name()) # test name
    
    if test.get_minValue() == -1 and test.get_maxValue() == -1:
        return False
    
    if test.get_minValue() != -1 and test.get_maxValue() != -1:
        return record.get_result() < test.get_minValue() or record.get_result() > test.get_maxValue()
    
    elif test.get_minValue() != -1:
        return record.get_result() < test.get_minValue()
    
    else:
        return record.get_result() > test.get_maxValue()

# its name is enough
def get_min_max_avg_value(dic):
    min, max, sum, rec_sum = [0, 0, 0, 0]
    for key, record in dic.items():
        if min == 0:
            min = dic[key][0].get_result()
        for i in record:
            rec_sum += 1
            if min > i.get_result():
                min = i.get_result()
            if max < i.get_result():
                max = i.get_result()
            sum += i.get_result()
    return [min, max, sum / rec_sum]

def get_min_max_avg_turn_Around():
    min, max, sum, rec_sum = [timedelta(0), timedelta(0), timedelta(0), 0]
    for key, record in dic.items():
        for i in record:
            test = get_test(i.get_name())
            day = int(test.get_days())
            hour = int(test.get_hour())
            minute = int(test.get_mins())
            turn_around = timedelta(days=day, hours=hour, minutes=minute)
            rec_sum += 1
            if min > turn_around or min == timedelta(0):
                min = turn_around
            if max < turn_around:
                max = turn_around
            sum += turn_around
            
    return [min, max, sum / rec_sum]

# filter choice
def filter():
        print("Enter -0- for things you don't want to filter and -1- (any numericall value might work tbh) for things you want\n")
        filter_list = []
        
        try:
            value = input("1-Patient ID ?\n")
            if value == "":
                print("The optoin set to be false")
                filter_list.append(0)
            else:
                filter_list.append((int(value)))

        except Exception:
            print("Enter just 0 for no and 1 for yes!")
            return None
        
        if filter_list[0] != 0:
            try:
                PID = (int(input("Enter Patient ID\n")))
            except Exception:
                print("not valid")
                return None
            if len(str(PID)) != 7:
                print("not valid length")
                return None
            
        try:
            value = (input("2-Test Name ?\n"))
            if value == "":
                print("The optoin set to be false")
                filter_list.append(0)
            else:
                filter_list.append((int(value)))
                
        except Exception:
            print("Enter just 0 for no and 1 for yes !")
            return None
        if filter_list[1] != 0:
            test_symbol = (input("Enter Test name\n"))
            if get_test(test_symbol) == None:
                print("Enter a valid test name")
                return None


        try:
            fvalue = input("3-Abnormal Test ?\n")
            if value == "":
                print("The optoin set to be false")
                filter_list.append(0)
            else:
                filter_list.append((int(value)))
                
        except Exception:
            print("Enter just 0 for no and 1 for yes !")
            return None

            
        try:
            value = input("4-Specific Period ?\n")
            if value == "":
                print("The optoin set to be false")
                filter_list.append(0)
            else:
                filter_list.append((int(value)))
                
            if filter_list[3] != 0:
                date1 = input("Enter the first Date, Format: YYYY-MM-DD HH:MM\n")
                date2 = input("Enter the second Date, Format: YYYY-MM-DD HH:MM\n")
                try:
                    record = Record(testsList[0].get_symbol(), "2024-01-01 11:11", "None", "None", "None", "2024-01-01 11:11")
                except Exception:
                    print("no valid tests")
                if is_in_period(date2, date1, record) == None:
                    print("Enter a valid dates")
                    return None 
            
        except Exception:
            print("Enter just 0 for no and 1 for yes !")
            return None
        
        try:
            value = input("5-Test Status ? \n")
            if value == "":
                print("The optoin set to be false")
                filter_list.append(0)
            else:
                filter_list.append((int(value)))
                
            if filter_list[4] != 0:
                try:
                    status = int(input("Enter test Status\n1-Completed\n2-Pending\n3-Reviewed\n"))
                except Exception:
                    print("Not valid status, enter a number")
                    return None
                
                if status < 1 or status > 3:
                    print("Not valid status")
                    return None
                
                if status == 1:
                    status_string = "completed"
                elif status == 2:
                    status_string = "pending"
                elif status == 3:
                    status_string = "reviewed"
                
        except Exception:
            print("Enter just 0 for no and 1 for yes !")
            return None

        try:
            value = input("6-Test turnaround time within a period ? \n")
            if value == "":
                print("The optoin set to be false")
                filter_list.append(0)
            else:
                filter_list.append((int(value)))
            if filter_list[5] != 0:
                date1 = input("Enter the first Date, format: DD-HH-MM\n")
                date2 = input("Enter the second Date, format: DD-HH-MM\n")
                try:
                    try:
                        record = Record(testsList[0].get_symbol(), "2024-01-01 11:11", "None", "None", "None", "2024-01-01 11:11")
                    except Exception:
                        print("no valid tests")
                    is_in_period_test_format(date1, date2, record)
                except Exception:
                    print("Not valid period")
                    return None
        except Exception:
            print("Enter just 0 for no and 1 for yes !")
            return None
        fo = open("MedicalRecords.txt", "r+")
        line1 = {}

        if filter_list[0] != 0:
            if PID in record_dict:
                line1[PID] = record_dict[PID]
        else:
            line1 = record_dict
        
        line2 = {}
        if filter_list[1] != 0:
            for key, record in line1.items():
                for i in record:
                    if i.get_name() == test_symbol:
                        if key in line2:
                            line2[key].append(i)
                        else:
                            line2[key] = [i]
        
        else:
            line2 = line1
        
        line3 = {}
        if filter_list[2] != 0:
            for key, record in line2.items():
                for i in record:
                    if is_abnormal(i) == True:
                        if key in line3:
                            line3[key].append(i)
                        else:
                            line3[key] = [i]
        else:
            line3 = line2

        line4 = {}
        if filter_list[3] != 0:
            for key, record in line3.items():
                for i in record:
                    if is_in_period(date1, date2, i) == True:
                        if key in line4:
                            line4[key].append(i)
                        else:
                            line4[key] = [i]
        else:
            line4 = line3
            
        line5 = {}
        if filter_list[4] != 0:
            for key, record in line4.items():
                for i in record:
                    if str(i.get_status()) == status_string:
                        print(i.get_status())
                        if key in line5:
                            line5[key].append(i)
                        else:
                            line5[key] = [i]
        else:
            line5 = line4

        line6 = {}
        if filter_list[5] != 0:
           for key, record in line5.items():
                for i in record:
                    if i.get_status() == "completed" and (is_in_period_test_format(date1, date2, i)) == True:
                        if key in line6:
                            line6[key].append(i)
                        else:
                            line6[key] = [i]
        else:
            line6 = line5
            
        return line6

#=============================
testsList = []
record_list = []
record_dict = {}
dic = {}
rec_dict = {}
creatMedicalTestList()
creat_medical_record_list()
#==============================

op = 1
filter_flag = False
while op > 0 and op < 10:
    if filter_flag != True:
        dic = record_dict
    try:
        op = int(input("\nEnter what operation you want based on number\n1- Add new Medical Test\n2-Add new Medical Record\n3-Update patient Record\n4-Update Medical Test\n5-Filter Medical Test\n6-Generate Texual Summary reports\n7-Export Medical Record\n8-Import Medical Record\n9-Delete Out dated records\n10-Exit\n"))
    except Exception:
        print("Enter a numerical value") 
        continue
    if op > 10 or op <= 0:
        print("Enter a valid value")
        op = 1
        continue

    if op == 1:
        add_new_medical_test()
    elif op == 2:
        add_new_medical_record()
    elif op == 3:
        update_medical_record()
    elif op == 4:
        update_medical_test()
    elif op == 5:
        dic = filter()
        filter_flag = True
        if dic == None:
            continue
        for key, record in dic.items():
            for i in record:
                print(str(key) + ": " + do_record_dict_format(i))
    
    elif op == 6:
        if dic == None:
            dic = record_dict
        min, max, avg = get_min_max_avg_value(dic)
        print("min= ", min, " max= ", max, " avg= ", avg)

        min, max, avg = get_min_max_avg_turn_Around()
        print("min= ", min, " max= ", max, " avg= ", avg)
    elif op == 7:
        write_on_csv()
    
    elif op == 8:
        import_from_csv()
        for key, record in rec_dict.items():
            for i in record:
                print(str(key) + ": " + do_record_dict_format(i))
        
    elif op == 9:
        delete_out_dated_records()

    creat_medical_record_list()
    

# creat_medical_record_list()
            