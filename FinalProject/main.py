import random
import mysql.connector
from faker import Faker
import csv
import pandas as pd
from pandas import DataFrame
import re

# connecting to the google cloud db
db = mysql.connector.connect(
    host="34.94.39.69",
    user="appuser",
    password="helloworld",
    database="Professors"
)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# mycursor allows python to execute SQL statements
mycursor = db.cursor()


# Generates information to populate the database using faker
def generateData():
    fake = Faker()
    subjects = {1: 'Computer Science', 2: 'Engineering', 3: 'Mathematics', 4: 'Physics'}
    cs_courses = {1: 'CPSC100', 2: 'CPSC215', 3: 'CPSC350', 4: 'CPSC400'}
    eng_courses = {1: 'ENG100', 2: 'ENG240', 3: 'ENG380', 4: 'ENG410'}
    math_courses = {1: 'MATH100', 2: 'MATH205', 3: 'MATH310', 4: 'MATH 400'}
    phy_courses = {1: 'PHY100', 2: 'PHY220', 3: 'PHY340', 4: 'PHY410'}
    comments = {1: 'I would recommend!', 2: 'Great professor!', 3: 'I love this course!', 4: 'Horrible professor'}

    csv_file = open("./allRecords.csv", "w")
    writer = csv.writer(csv_file)

    # inputting header in the csv file
    writer.writerow(
        ["FirstName", "LastName", "Subject", "Course", "UserEmail", "Rate", "Comment", "IsDeleted"])

    isDeleted = 0

    # generating data using faker
    for x in range(0, 40):
        rate = str(random.randint(1, 4)) + '.' + str(random.randint(0, 9))
        subject = subjects.get(random.randint(1, 4))
        course1 = cs_courses.get(random.randint(1, 4))
        course2 = eng_courses.get(random.randint(1, 4))
        course3 = math_courses.get(random.randint(1, 4))
        course4 = phy_courses.get(random.randint(1, 4))
        comment = comments.get(random.randint(1, 4))

        if subject == 'Computer Science':
            writer.writerow([fake.first_name(), fake.last_name(), subject, course1, fake.email(), rate, comment,
                             isDeleted])
        elif subject == 'Engineering':
            writer.writerow([fake.first_name(), fake.last_name(), subject, course2, fake.email(), rate, comment,
                             isDeleted])
        elif subject == 'Mathematics':
            writer.writerow([fake.first_name(), fake.last_name(), subject, course3, fake.email(), rate, comment,
                             isDeleted])
        else:
            writer.writerow([fake.first_name(), fake.last_name(), subject, course4, fake.email(), rate, comment,
                             isDeleted])

    # print("Generated data successfully")


# importing data to the normalized tables
def importAllData():
    with open("./allRecords.csv") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            mycursor.execute("INSERT INTO Subject(SubjectName) "
                             "VALUES (%s) ; ", (row['Subject'],))
            db.commit()

            subId = mycursor.lastrowid

            mycursor.execute("INSERT INTO User(UserEmail, DeletedUser) "
                             "VALUES (%s, %s) ; ", (row['UserEmail'], row['IsDeleted']))
            db.commit()

            userId = mycursor.lastrowid

            mycursor.execute("INSERT INTO Professor(FirstName, LastName) "
                             "VALUES (%s, %s); ", (row['FirstName'], row['LastName']))
            db.commit()

            profId = mycursor.lastrowid
            # ProfessorCourse
            mycursor.execute("INSERT INTO Course(ProfessorId, SubjectId, CourseName) "
                             "VALUES (%s, %s, %s); ", (profId, subId, row['Course']))
            db.commit()

            courseId = mycursor.lastrowid
            mycursor.execute("INSERT INTO Rate(ProfessorId, SubjectId, CourseId, UserId, RateNumber, UserComment) "
                             "VALUES (%s, %s, %s, %s, %s, %s); ",
                             (profId, subId, courseId, userId, row['Rate'], row['Comment']))
            db.commit()

    # print("Import data successfully")


# main menu
def mainMenu():
    choice = int(input("""
Main Menu
1: Display records
2: Insert
3: Update 
4: Delete
5: Search
6: Generate Reports
7: Quit

Enter your choice: """))

    if choice == 1:
        displayRecordsMenu()
        mainMenu()

    elif choice == 2:
        insertReview()
        mainMenu()

    elif choice == 3:
        updateMenu()
        mainMenu()

    elif choice == 4:
        deleteUser()
        mainMenu()

    elif choice == 5:
        searchMenu()
        mainMenu()

    elif choice == 6:
        generateReportMenu()
        mainMenu()

    elif choice == 7:
        exit()

    else:
        print("Invalid input")
        print("Select 1, 2, 3, 4, 5, 6")
        mainMenu()


# display sub menu
def displayRecordsMenu():
    choice = int(input("""
Display  
1: All records
2: User Information
3: Main Menu
4: Quit
        
Enter your choice: """))

    if choice == 1:
        mycursor.execute("SELECT * FROM vProfessorInfo")

        allRecords = mycursor.fetchall()
        df = DataFrame(allRecords, columns=['ProfessorId', 'FirstName', 'LastName', 'Subject', 'Course', 'UserId',
                                            'UserEmail', 'Rate', 'Comment', 'IsDeleted'])
        print(df)
        db.commit()

        displayRecordsMenu()

    elif choice == 2:
        mycursor.execute("SELECT UserId, UserEmail, FirstName, LastName, CourseName, RateNumber, UserComment, "
                         "DeletedUser "
                         "FROM vProfessorInfo ")

        subjectRecord = mycursor.fetchall()
        df = DataFrame(subjectRecord,
                       columns=['UserId', 'UserEmail', 'ProfFirstName', 'ProfLastName', 'Course', 'Rate', 'Review',
                                'IsDeleted'])
        print(df)
        db.commit()

        displayRecordsMenu()

    elif choice == 3:
        mainMenu()

    elif choice == 4:
        exit()

    else:
        print("Invalid input")
        print("Going back to main menu...")
        mainMenu()


# insert review
def insertReview():
    print("\nCreate a review")
    userEmail = input("Enter your email: ")

    if userEmail.__contains__("@") and userEmail.__contains__("."):
        pass
    else:
        print("\nError: Enter invalid email")
        print("Returning to main menu...")
        mainMenu()

    fn = input("Enter Professor's first name: ")
    if not fn.isalpha():
        print("Invalid input")
        print("Returning back to main menu...")
        mainMenu()

    ln = input("Enter P1rofessor's last name: ")
    if not ln.isalpha():
        print("Invalid input")
        print("Returning back to main menu...")
        mainMenu()

    print("Subjects: Computer Science, Engineering, Mathematics, Physics")
    subject = input("Enter the subject: ")
    if (subject == 'Computer Science' or subject == 'Engineering' or
            subject == 'Mathematics' or subject == 'Physics'):
        pass
    else:
        print("Invalid input")
        print("Returning back to main menu...")
        mainMenu()

    course = input("Enter the course: ")
    for i in subject:
        if i != ' ' and i.isdigit():
            print("Invalid input")
            print("Returning back to main menu...")
            mainMenu()

    print("Rate 1 through 5, 1 being the lowest and 5 being the highest")
    rateStr = input("Enter rate: ")
    rate = float(rateStr)
    if rate >= 1.0 and rate <= 5.0:
        pass
    else:
        print("Invalid input")
        print("Returning back to main menu...")
        mainMenu()

    comment = input("Enter comment: ")

    mycursor.execute("INSERT INTO Subject(SubjectName) "
                     "VALUES (%s) ; ", (subject,))
    db.commit()

    subId = mycursor.lastrowid
    isDeleted = 0
    mycursor.execute("INSERT INTO User(UserEmail, DeletedUser) "
                     "VALUES (%s, %s) ; ", (userEmail, isDeleted))
    db.commit()

    userId = mycursor.lastrowid

    mycursor.execute("INSERT INTO Professor(FirstName, LastName) "
                     "VALUES (%s, %s); ", (fn, ln))
    db.commit()

    profId = mycursor.lastrowid
    mycursor.execute("INSERT INTO Course(ProfessorId, SubjectId, CourseName) "
                     "VALUES (%s, %s, %s); ", (profId, subId, course))
    db.commit()

    courseId = mycursor.lastrowid
    mycursor.execute("INSERT INTO Rate(ProfessorId, SubjectId, CourseId, UserId, RateNumber, UserComment) "
                     "VALUES (%s, %s, %s, %s, %s, %s); ",
                     (profId, subId, courseId, userId, rate, comment))
    db.commit()

    print("Thanks for the review!")


# update sub menu
def updateMenu():
    choice = int(input("""
Update 
1: Email
2: Comment
3: Main Menu
4: Quit

Enter your choice: """))

    if choice == 1:
        userId = input("Enter your user id: ")
        if userId.isdigit():
            pass
        else:
            print("Invalid input")
            print("Returning back the update menu...")
            updateMenu()

        updateEmail = input("Enter email: ")

        if updateEmail.__contains__("@") and updateEmail.__contains__("."):
            pass
        else:
            print("Invalid input")
            print("Returning to update menu...")
            updateMenu()

        mycursor.execute("UPDATE User SET UserEmail = (%s) WHERE UserId = (%s) ;", (updateEmail, userId))
        db.commit()

        print("Update success")

    elif choice == 2:
        userId = input("Enter your user id: ")
        if userId.isdigit():
            pass
        else:
            print("Invalid input")
            print("Returning back the update menu...")
            updateMenu()

        updateComment = input("Enter comment : ")

        mycursor.execute("UPDATE Rate SET UserComment = (%s) WHERE UserId = (%s) ;", (updateComment, userId))
        db.commit()

        print("Update success")

    elif choice == 3:
        mainMenu()

    else:
        print("Invalid input")
        print("Returning back the update menu...")
        updateMenu()


# delete user
def deleteUser():
    deleted = 1
    choice = input("Are you sure you would like to delete account from the database? "
                   "Enter yes or no: ")
    if choice == "Yes" or choice == "yes":
        userId = input("Enter user id: ")
        if userId.isdigit():
            pass
        else:
            print("Invalid input")
            print("Returning back the main menu...")
            mainMenu()

        mycursor.execute("UPDATE User SET DeletedUser = (%s) WHERE UserId = (%s) ;", (deleted, userId))
        db.commit()

        print("Delete success")

    elif choice == "No" or choice == "no":
        print("Returning back to main menu...")
        mainMenu()

    else:
        print("Invalid input")
        print("Returning back to main menu...")
        mainMenu()


# search sub menu
def searchMenu():
    choice = int(input("""
Search/Display 
1: Subject
2: Rates 
3: Main Menu 
4: Quit

Enter your choice: """))

    if choice == 1:
        print("Subjects: Computer Science, Engineering, Math, or Physics")
        subject = input("Enter the subject: ")

        if subject == "Computer Science" or subject == "computer science":
            mycursor.execute("SELECT FirstName, LastName, CourseName, RateNumber, UserComment "
                             "FROM Rate "
                             "INNER JOIN Professor ON Rate.ProfessorId = Professor.ProfessorId "
                             "INNER JOIN Course ON Rate.CourseId = Course.CourseId "
                             "INNER JOIN Subject ON Rate.SubjectId = Subject.SubjectId "
                             "INNER JOIN User ON Rate.UserId = User.UserId "
                             "WHERE SubjectName = 'Computer Science' and DeletedUser = 0 "
                             "ORDER BY CourseName asc ")

            csCourse = mycursor.fetchall()
            df = DataFrame(csCourse, columns=['FirstName', 'LastName', 'Course', 'Rate', 'Comment'])
            print(df)
            db.commit()


        elif subject == "Engineering" or subject == "engineering":
            mycursor.execute("SELECT FirstName, LastName, CourseName, RateNumber, UserComment "
                             "FROM Rate "
                             "INNER JOIN Professor ON Rate.ProfessorId = Professor.ProfessorId "
                             "INNER JOIN Course ON Rate.CourseId = Course.CourseId "
                             "INNER JOIN Subject On Rate.SubjectId = Subject.SubjectId "
                             "WHERE SubjectName = 'Engineering' and DeletedUser = 0 "
                             "ORDER BY CourseName asc ")

            csCourse = mycursor.fetchall()
            df = DataFrame(csCourse, columns=['FirstName', 'LastName', 'Courses', 'Rate', 'Comment'])
            print(df)
            db.commit()

        elif subject == "Math" or subject == "math":
            mycursor.execute("SELECT FirstName, LastName, CourseName, RateNumber, UserComment "
                             "FROM Rate "
                             "INNER JOIN Professor ON Rate.ProfessorId = Professor.ProfessorId "
                             "INNER JOIN Course ON Rate.CourseId = Course.CourseId "
                             "INNER JOIN Subject On Rate.SubjectId = Subject.SubjectId "
                             "WHERE SubjectName = 'Math' and DeletedUser = 0 "
                             "ORDER BY CourseName asc ")

            csCourse = mycursor.fetchall()
            df = DataFrame(csCourse, columns=['FirstName', 'LastName', 'Courses', 'Rate', 'Comment'])
            print(df)
            db.commit()

        elif subject == "Physics" or subject == "physics":
            mycursor.execute("SELECT FirstName, LastName, CourseName, RateNumber, UserComment "
                             "FROM Rate "
                             "INNER JOIN Professor ON Rate.ProfessorId = Professor.ProfessorId "
                             "INNER JOIN Course ON Rate.CourseId = Course.CourseId "
                             "INNER JOIN Subject On Rate.SubjectId = Subject.SubjectId "
                             "WHERE SubjectName = 'Physics' and DeletedUser = 0 "
                             "ORDER BY CourseName asc ")

            csCourse = mycursor.fetchall()
            df = DataFrame(csCourse, columns=['FirstName', 'LastName', 'Courses', 'Rate', 'Comment'])
            print(df)
            db.commit()


        else:
            print("Enter Computer Science, Engineering, Math, or Physics")
            searchMenu()

    elif choice == 2:
        searchRate = int(input("Enter the rate (1-5): "))
        if searchRate >= 1 and searchRate <= 5:
            pass
        else:
            print("Invalid input")
            print("Returning back the update menu...")
            searchMenu()

        if searchRate == 1:
            mycursor.execute("SELECT FirstName, LastName, CourseName, RateNumber, UserComment "
                             "FROM Rate "
                             "INNER JOIN Professor ON Rate.ProfessorId = Professor.ProfessorId "
                             "INNER JOIN Course ON Rate.CourseId = Course.CourseId "
                             "INNER JOIN User ON Rate.UserId = User.UserId "
                             "WHERE Rate.ProfessorId IN (SELECT Rate.ProfessorId "
                             "FROM Rate "
                             "WHERE RateNumber >= 1.0 and RateNumber < 2.0 and DeletedUser = 0) "
                             "ORDER BY RateNumber asc ")

            courseRecord = mycursor.fetchall()
            df = DataFrame(courseRecord, columns=['FirstName', 'LastName', 'Courses', 'Rate', 'UserComment'])
            print(df)
            db.commit()


        elif searchRate == 2:
            mycursor.execute("SELECT FirstName, LastName, CourseName, RateNumber, UserComment "
                             "FROM Rate "
                             "INNER JOIN Professor ON Rate.ProfessorId = Professor.ProfessorId "
                             "INNER JOIN Course ON Rate.CourseId = Course.CourseId "
                             "INNER JOIN User ON Rate.UserId = User.UserId "
                             "WHERE Rate.ProfessorId IN (SELECT Rate.ProfessorId "
                             "FROM Rate "
                             "WHERE RateNumber >= 2.0 and RateNumber < 3.0 and DeletedUser = 0) "
                             "ORDER BY RateNumber asc ")

            courseRecord = mycursor.fetchall()
            df = DataFrame(courseRecord, columns=['FirstName', 'LastName', 'Courses', 'Rate', 'UserComment'])
            print(df)
            db.commit()


        elif searchRate == 3:
            mycursor.execute("SELECT FirstName, LastName, CourseName, RateNumber, UserComment "
                             "FROM Rate "
                             "INNER JOIN Professor ON Rate.ProfessorId = Professor.ProfessorId "
                             "INNER JOIN Course ON Rate.CourseId = Course.CourseId "
                             "INNER JOIN User ON Rate.UserId = User.UserId "
                             "WHERE Rate.ProfessorId IN (SELECT Rate.ProfessorId "
                             "FROM Rate "
                             "WHERE RateNumber >= 3.0 and RateNumber < 4.0 and DeletedUser = 0) "
                             "ORDER BY RateNumber asc ")

            courseRecord = mycursor.fetchall()
            df = DataFrame(courseRecord, columns=['FirstName', 'LastName', 'Courses', 'Rate', 'UserComment'])
            print(df)
            db.commit()


        elif searchRate == 4:
            mycursor.execute("SELECT FirstName, LastName, CourseName, RateNumber, UserComment "
                             "FROM Rate "
                             "INNER JOIN Professor ON Rate.ProfessorId = Professor.ProfessorId "
                             "INNER JOIN Course ON Rate.CourseId = Course.CourseId "
                             "INNER JOIN User ON Rate.UserId = User.UserId "
                             "WHERE Rate.ProfessorId IN (SELECT Rate.ProfessorId "
                             "FROM Rate "
                             "WHERE RateNumber >= 4.0 and RateNumber < 5.0 and DeletedUser = 0) "
                             "ORDER BY RateNumber asc ")

            courseRecord = mycursor.fetchall()
            df = DataFrame(courseRecord, columns=['FirstName', 'LastName', 'Courses', 'Rate', 'UserComment'])
            print(df)
            db.commit()


        elif searchRate == 5:
            mycursor.execute("SELECT FirstName, LastName, CourseName, RateNumber, UserComment "
                             "FROM Rate "
                             "INNER JOIN Professor ON Rate.ProfessorId = Professor.ProfessorId "
                             "INNER JOIN Course ON Rate.CourseId = Course.CourseId "
                             "INNER JOIN User ON Rate.UserId = User.UserId "
                             "WHERE Rate.ProfessorId IN (SELECT Rate.ProfessorId "
                             "FROM Rate "
                             "WHERE RateNumber = 5.0 and DeletedUser = 0) "
                             "ORDER BY RateNumber asc ")

            courseRecord = mycursor.fetchall()
            df = DataFrame(courseRecord, columns=['FirstName', 'LastName', 'Courses', 'Rate', 'UserComment'])
            print(df)
            db.commit()


        else:
            print("Invalid input...")
            print("Return to search menu...")
            searchMenu()

    elif choice == 3:
        mainMenu()

    elif choice == 4:
        exit()

    else:
        print("Invalid input...")
        print("Return to search menu...")
        searchMenu()


# generating report sub menu
def generateReportMenu():
    choice = int(input("""
Generate Reports 
1: Deleted user records
2: Average Rate of courses
3: Import all reports
4: Main menu
5: Quit

Enter your choice: """))

    if choice == 1:
        importDeleteData()

    elif choice == 2:
        importAverageRateCoursesData()

    elif choice == 3:
        importDeleteData()
        importAverageRateCoursesData()
        print("Imported all reports successfully")

    elif choice == 4:
        mainMenu()

    elif choice == 5:
        exit()

    else:
        print("Invalid input...")
        print("Return to search menu... ")
        generateReportMenu()


# import delete user report
def importDeleteData():
    query = mycursor.execute("SELECT UserId, UserEmail "
                             "FROM User "
                             "WHERE DeletedUser = 1 ")
    mycursor.execute(query)
    csv_file = open("./DeletedUserReport.csv", "w")
    writer = csv.writer(csv_file)

    # inputting header in the csv file
    writer.writerow(["UserId", "UserEmail"])

    print("Import data successfully")

    for row in mycursor:
        writer.writerow(row)

    db.commit()

# import average rate course report
def importAverageRateCoursesData():
    query = mycursor.execute("SELECT CourseName, CAST(AVG(RateNumber) AS DECIMAL (3,1)) "
                             "FROM Rate "
                             "INNER JOIN Course ON Rate.CourseId = Course.CourseId "
                             "GROUP BY CourseName ")

    mycursor.execute(query)
    csv_file = open("./AvgRateCoursesReport.csv", "w")
    writer = csv.writer(csv_file)

    # inputting header in the csv file
    writer.writerow(["Course", "AvgRate"])

    print("Import data successfully")

    for row in mycursor:
        writer.writerow(row)

    db.commit()


# ==================================================================
# main
generateData()
importAllData()
mainMenu()
