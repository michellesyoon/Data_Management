import sqlite3
# formatting outputs
import pandas as pd
from pandas import DataFrame
import re

# https://thispointer.com/python-pandas-how-to-display-full-dataframe-i-e-print-all-rows-columns-without-truncation/
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# establishing a connection to the db
conn = sqlite3.connect('./Student.db')

# myCursor allows python to execute SQL statements
myCursor = conn.cursor()

# 2a) Write a python function to import the students.csv file
# into your newly created Students table
# https://www.w3schools.com/python/pandas/pandas_dataframes.asp
myCursor.execute("SELECT * FROM Student")
StudentTable = myCursor.fetchall()
df = pd.read_csv("./students.csv")

if not StudentTable:
    for i in StudentTable:
        myCursor.execute("UPDATE Student SET isDeleted = 0")

    df.to_sql("Student", conn, if_exists='append', index=False)


def mainMenu():
    choice = input("""
    Main Menu
    A: Display student records
    B: Insert
    C: Update 
    D: Delete
    E: Search
    F: Quit
    Enter your choice: """)

    if choice == "A" or choice == "a":
        displayStudentRecords()
        mainMenu()

    elif choice == "B" or choice == "b":
        insertStudent()
        mainMenu()

    elif choice == "C" or choice == "c":
        updateMenu()
        mainMenu()

    elif choice == "D" or choice == "d":
        deleteStudent()
        mainMenu()

    elif choice == "E" or choice == "e":
        searchMenu()

    elif choice == "F" or choice == "f":
        exit()

    else:
        print("""    Invalid input""")
        print("""    Select A, B, C, D, E, F""")
        mainMenu()


def updateMenu():
    choice = input("""
        Update 
        A: Major
        B: Advisor
        C: Mobile Phone Number
        D: Main Menu
        E: Quit
        Enter your choice: """)

    if choice == "A" or choice == "a":
        updateStudentMajor()
        updateMenu()

    elif choice == "B" or choice == "b":
        updateStudentAdvisor()
        updateMenu()

    elif choice == "C" or choice == "c":
        updateStudentMobileNum()
        updateMenu()

    elif choice == "D" or choice == "d":
        mainMenu()

    elif choice == "E" or choice == "e":
        exit()

    else:
        print("""
            Select A, B, C, E, F""")
        updateMenu()


def searchMenu():
    choice = input("""
            Search/Display 
            A: Major
            B: GPA 
            C: City 
            D: State
            E: Faculty Advisor
            F: Main Menu
            G: Quit
            Enter your choice: """)

    if choice == "A" or choice == "a":
        print("Enter Communications, Computer Science, History, Math, or Physics")
        searchMajor = input("Enter the major: ")
        for i in searchMajor:
            if i != ' ' and i.isdigit():
                print("Invalid input")
                searchMenu()
        if searchMajor == "Computer Science" or searchMajor == "computer science":
            searchDisplayMajorCompSci()
        elif searchMajor == "Communications" or searchMajor == "communications":
            searchDisplayMajorComm()
            searchMenu()
        elif searchMajor == "History" or searchMajor == "history":
            searchDisplayMajorHistory()
            searchMenu()
        elif searchMajor == "Math" or searchMajor == "math":
            searchDisplayMajorMath()
            searchMenu()
        elif searchMajor == "Physics" or searchMajor == "physics":
            searchDisplayMajorPhysics()
            searchMenu()
        else:
            print("Invalid input")
            print("Returning back to Search/Display menu...")
            searchMenu()

    elif choice == "B" or choice == "b":
        print("Enter 1 to display GPAs from 1.0 to 1.9")
        print("Enter 2 to display GPAs from 2.0 to 2.9")
        print("Enter 3 to display GPAs from 3.0 to 3.9")
        print("Enter 4 to display GPAs from 4.0 to 4.9")
        choiceStr = input("Enter: ")
        choice = int(choiceStr)

        if choice == 1:
            searchGPAOne()
            searchMenu()
        elif choice == 2:
            searchGPATwo()
            searchMenu()
        elif choice == 3:
            searchGPAThree()
            searchMenu()
        elif choice == 4:
            searchGPAFour()
            searchMenu()
        else:
            print("Invalid input")
            print("Returning back to Search/Display menu...")
            searchMenu()

    elif choice == "C" or choice == "c":
        searchCity()
        searchMenu()

    elif choice == "D" or choice == "d":
        searchState()
        searchMenu()

    elif choice == "E" or choice == "e":
        searchFAdvisor()
        searchMenu()

    elif choice == "F" or choice == "f":
        mainMenu()

    elif choice == "G" or choice == "g":
        exit()

    else:
        print("""
                Select A, B, C, E, F""")
        updateMenu()


# 2b) Display All Students and all of their attributes.
#   i.Create the necessary SELECT statement to produce this
#   result to standard output
def displayStudentRecords():
    myCursor.execute("SELECT * FROM Student")
    displayInfo()


# 2c) Add NewStudents
#   i.All attributes are required when creating a new student.
#   ii.Please make sure to validate user input appropriately.
def insertStudent():
    print("Enter student information")
    fn = input("First name: ")
    if not fn.isalpha():
        print("Invalid input")
        mainMenu()

    ln = input("Last name: ")
    if not ln.isalpha():
        print("Invalid input")
        mainMenu()

    gpaStr = input("GPA: ")
    gpa = float(gpaStr)
    if not 0.0 >= gpa and 4.5 <= gpa:
        print("GPA is scaled from 0.0 to 4.0")
        mainMenu()

    major = input("Major: ")
    for i in major:
        if i != ' ' and i.isdigit():
            print("Invalid input")
            mainMenu()

    fAdvisor = input("Faculty Advisor: ")
    for i in fAdvisor:
        if i != ' ' and i.isdigit():
            print("Invalid input")
            mainMenu()

    address = input("Address: ")

    city = input("City: ")
    for i in city:
        if i != ' ' and i.isdigit():
            print("Invalid input")
            mainMenu()

    state = input("State: ")
    for i in state:
        if i != ' ' and i.isdigit():
            print("Invalid input")
            mainMenu()

    zCode = input("Zip Code: ")
    if not zCode.isdigit():
        print("Invalid input")
        mainMenu()

    mobileNum = input("Mobile Number: ")
    pattern1 = "^\((\d{3})\) (\d{3})-(\d{4}) (\w+)$"
    pattern2 = "^\((\d{3})\) (\d{3})-(\d{4})$"

    isMobileNum1 = re.match(pattern1, mobileNum)
    isMobileNum2 = re.match(pattern2, mobileNum)
    if not (isMobileNum1 or isMobileNum2):
        print("Invalid, format (XXX) XXX-XXX extXXX..-extension is optional")
        print("Invalid input")
        mainMenu()

    myCursor.execute("INSERT INTO Student (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, "
                     "ZipCode, MobilePhoneNumber) VALUES (?,?,?,?,?,?,?,?,?,?)", (fn, ln, gpa, major, fAdvisor, address,
                                                                                  city, state, zCode, mobileNum))
    conn.commit()


# 2d) Update Students
#   i.Only the following fields can be updated 1.Major, Advisor, MobilePhoneNumber
#   ii.Make sure that your UPDATE statement makes use of the correct key


def updateStudentMajor():
    sId = input("Enter Student ID: ")
    if not sId.isdigit():
        print("Invalid input")
        print("Returning back the update menu...")
        updateMenu()

    updateMajor = input("Major: ")
    for i in updateMajor:
        if i != ' ' and i.isdigit():
            print("Invalid input")
            updateMenu()
    myCursor.execute("UPDATE Student SET Major = ? WHERE StudentId = ?", (updateMajor, sId))
    conn.commit()


def updateStudentAdvisor():
    sId = input("Enter Student ID: ")
    if not sId.isdigit():
        print("Invalid input")
        print("Returning back the update menu...")
        updateMenu()

    updateAdvisor = input("Faculty Advisor: ")
    for i in updateAdvisor:
        if i != ' ' and i.isdigit():
            print("Invalid input")
            updateMenu()
    myCursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?", (updateAdvisor, sId))
    conn.commit()


def updateStudentMobileNum():
    sId = input("Enter Student ID: ")
    if not sId.isdigit():
        print("Invalid input")
        print("Returning back the update menu...")
        updateMenu()

    updateMobileNum = input("Mobile Phone Number: ")
    pattern1 = "^\((\d{3})\) (\d{3})-(\d{4}) (\w+)$"
    pattern2 = "^\((\d{3})\) (\d{3})-(\d{4})$"

    isMobileNum1 = re.match(pattern1, updateMobileNum)
    isMobileNum2 = re.match(pattern2, updateMobileNum)
    if not (isMobileNum1 or isMobileNum2):
        print("Invalid, format (XXX) XXX-XXX extXXX..-extension is optional")
        print("Invalid input")
        updateMenu()

    myCursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ?", (updateMobileNum, sId))
    conn.commit()


# Delete Students by StudentId
#   i.Perform a “soft”delete on students that is, set isDeleted to true(1)
def deleteStudent():
    deleted = 1
    choice = input("    Are you sure you would like to delete this student from the database? "
                   "Enter yes or no: ")
    if choice == "Yes" or choice == "yes":
        sId = input("    Enter Student ID: ")
        if not sId.isdigit():
            print("Invalid input")
            print("Returning back the update menu...")
            updateMenu()

        myCursor.execute("UPDATE Student SET isDeleted = ? WHERE StudentId = ?", (deleted, sId))
        conn.commit()
    elif choice == "No" or choice == "no":
        print("    Returning back to update menu...")
        updateMenu()
    else:
        print("    Invalid input\n")
        deleteStudent()


# Search/Display students by Major, GPA, City, State and Advisor.
#   i.User should be able to query by the 5 aforementioned fields
def searchDisplayMajorCompSci():
    myCursor.execute("SELECT * FROM Student WHERE Major IN ('Computer Science')")
    displayInfo()


def searchDisplayMajorComm():
    myCursor.execute("SELECT * FROM Student WHERE Major IN ('Communications')")
    displayInfo()


def searchDisplayMajorHistory():
    myCursor.execute("SELECT * FROM Student WHERE Major IN ('History')")
    displayInfo()


def searchDisplayMajorMath():
    myCursor.execute("SELECT * FROM Student WHERE Major IN ('Math')")
    displayInfo()


def searchDisplayMajorPhysics():
    myCursor.execute("SELECT * FROM Student WHERE Major IN ('Physics')")
    displayInfo()


def searchGPAOne():
    myCursor.execute("SELECT * FROM Student GROUP BY GPA HAVING (GPA >= 0.0 AND GPA <= 1.9)")
    displayInfo()


def searchGPATwo():
    myCursor.execute("SELECT * FROM Student GROUP BY GPA HAVING (GPA >= 2.0 AND GPA <= 2.9)")
    displayInfo()


def searchGPAThree():
    myCursor.execute("SELECT * FROM Student GROUP BY GPA HAVING (GPA >= 3.0 AND GPA <= 3.9)")
    displayInfo()


def searchGPAFour():
    myCursor.execute("SELECT * FROM Student GROUP BY GPA HAVING (GPA >= 4.0 AND GPA <= 4.9)")
    displayInfo()


def searchCity():
    choice = input("Enter the first character of the city name: ")
    choice.islower()

    if choice == 'a':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'A%' ")
        displayInfo()
    elif choice == 'b':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'B%' ")
        displayInfo()
    elif choice == 'c':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'C%' ")
        displayInfo()
    elif choice == 'd':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'D%' ")
        displayInfo()
    elif choice == 'e':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'E%' ")
        displayInfo()
    elif choice == 'f':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'F%' ")
        displayInfo()
    elif choice == 'g':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'G%' ")
        displayInfo()
    elif choice == 'h':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'H%' ")
        displayInfo()
    elif choice == 'i':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'I%' ")
        displayInfo()
    elif choice == 'j':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'J%' ")
        displayInfo()
    elif choice == 'k':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'K%' ")
        displayInfo()
    elif choice == 'l':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'L%' ")
        displayInfo()
    elif choice == 'm':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'M%' ")
        displayInfo()
    elif choice == 'n':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'M%' ")
        displayInfo()
    elif choice == 'o':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'O%' ")
        displayInfo()
    elif choice == 'p':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'P%' ")
        displayInfo()
    elif choice == 'q':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'Q%' ")
        displayInfo()
    elif choice == 'r':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'R%' ")
        displayInfo()
    elif choice == 's':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'S%' ")
        displayInfo()
    elif choice == 't':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'T%' ")
        displayInfo()
    elif choice == 'u':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'U%' ")
        displayInfo()
    elif choice == 'v':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'V%' ")
        displayInfo()
    elif choice == 'w':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'W%' ")
        displayInfo()
    elif choice == 'x':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'X%' ")
        displayInfo()
    elif choice == 'y':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'Y%' ")
        displayInfo()
    elif choice == 'z':
        myCursor.execute("SELECT * FROM Student WHERE City Like 'Z%' ")
        displayInfo()
    else:
        print("Invalid input")
        print("Returning back to search/display menu...")


def searchState():
    choice = input("Enter the first character of the state: ")
    choice.islower()

    if choice == 'a':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'A%' ")
        displayInfo()
    elif choice == 'b':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'B%' ")
        displayInfo()
    elif choice == 'c':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'C%' ")
        displayInfo()
    elif choice == 'd':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'D%' ")
        displayInfo()
    elif choice == 'e':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'E%' ")
        displayInfo()
    elif choice == 'f':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'F%' ")
        displayInfo()
    elif choice == 'g':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'G%' ")
        displayInfo()
    elif choice == 'h':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'H%' ")
        displayInfo()
    elif choice == 'i':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'I%' ")
        displayInfo()
    elif choice == 'j':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'J%' ")
        displayInfo()
    elif choice == 'k':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'K%' ")
        displayInfo()
    elif choice == 'l':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'L%' ")
        displayInfo()
    elif choice == 'm':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'M%' ")
        displayInfo()
    elif choice == 'n':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'M%' ")
        displayInfo()
    elif choice == 'o':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'O%' ")
        displayInfo()
    elif choice == 'p':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'P%' ")
        displayInfo()
    elif choice == 'q':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'Q%' ")
        displayInfo()
    elif choice == 'r':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'R%' ")
        displayInfo()
    elif choice == 's':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'S%' ")
        displayInfo()
    elif choice == 't':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'T%' ")
        displayInfo()
    elif choice == 'u':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'U%' ")
        displayInfo()
    elif choice == 'v':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'V%' ")
        displayInfo()
    elif choice == 'w':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'W%' ")
        displayInfo()
    elif choice == 'x':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'X%' ")
        displayInfo()
    elif choice == 'y':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'Y%' ")
        displayInfo()
    elif choice == 'z':
        myCursor.execute("SELECT * FROM Student WHERE State Like 'Z%' ")
        displayInfo()
    else:
        print("Invalid input")
        print("Returning back to search/display menu...")


def searchFAdvisor():
    choice = input("Enter the first character of the faculty advisor's first name: ")
    choice.islower()

    if choice == 'a':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'A%' ")
        displayInfo()
    elif choice == 'b':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'B%' ")
        displayInfo()
    elif choice == 'c':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'C%' ")
        displayInfo()
    elif choice == 'd':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'D%' ")
        displayInfo()
    elif choice == 'e':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'E%' ")
        displayInfo()
    elif choice == 'f':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'F%' ")
        displayInfo()
    elif choice == 'g':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'G%' ")
        displayInfo()
    elif choice == 'h':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'H%' ")
        displayInfo()
    elif choice == 'i':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'I%' ")
        displayInfo()
    elif choice == 'j':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'J%' ")
        displayInfo()
    elif choice == 'k':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'K%' ")
        displayInfo()
    elif choice == 'l':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'L%' ")
        displayInfo()
    elif choice == 'm':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'M%' ")
        displayInfo()
    elif choice == 'n':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'M%' ")
        displayInfo()
    elif choice == 'o':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'O%' ")
        displayInfo()
    elif choice == 'p':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'P%' ")
        displayInfo()
    elif choice == 'q':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'Q%' ")
        displayInfo()
    elif choice == 'r':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'R%' ")
        displayInfo()
    elif choice == 's':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'S%' ")
        displayInfo()
    elif choice == 't':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'T%' ")
        displayInfo()
    elif choice == 'u':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'U%' ")
        displayInfo()
    elif choice == 'v':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'V%' ")
        displayInfo()
    elif choice == 'w':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'W%' ")
        displayInfo()
    elif choice == 'x':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'X%' ")
        displayInfo()
    elif choice == 'y':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'Y%' ")
        displayInfo()
    elif choice == 'z':
        myCursor.execute("SELECT * FROM Student WHERE FacultyAdvisor Like 'Z%' ")
        displayInfo()
    else:
        print("Invalid input")
        print("Returning back to search/display menu...")




def displayInfo():
    conn.commit()
    record = myCursor.fetchall()
    df = DataFrame(record, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor',
                                    'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted'])
    print(df)


# ================================ Main ===========================
mainMenu()
