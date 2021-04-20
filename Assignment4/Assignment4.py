import mysql.connector
from faker import Faker
import csv

# connecting to the google cloud db
db = mysql.connector.connect(
    host="34.94.39.69",
    user="appuser",
    password="helloworld",
    database="Professors"
)


def generateData():
    fake = Faker()

    # creating the csv filename from user
    filename = input("Enter a filename (ex: filename.csv): ")

    if not filename.__contains__(".csv"):
        print("Error: Enter invalid filename")
        print("Exiting...")
        quit()

    final_filename = "./" + filename
    csv_file = open(final_filename, "w")
    writer = csv.writer(csv_file)

    # inputting header in the csv file
    writer.writerow(
        ["FirstName", "LastName", "Street", "City", "State", "Zip", "Month", "Day", "Year", "AdvisorFirstName",
         "AdvisorLastName"])

    # getting the number of records from user
    numRecordsStr = input("Enter the number of records: ")
    numRecords = int(numRecordsStr)

    # generating data using faker
    for x in range(0, numRecords):
        writer.writerow(
            [fake.first_name(), fake.last_name(), fake.street_address(), fake.city(), fake.state(), fake.zipcode(),
             fake.month(), fake.day_of_month(), fake.year(), fake.first_name(), fake.last_name()])
    print("Generated data successfully")


def importData():
    mycursor = db.cursor()
    with open("./mydata.csv") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            print("importing students")

            # importing the unstructured data from the csv file to the normalized db
            # StudentName db
            mycursor.execute("INSERT INTO StudentName(FirstName, LastName) "
                             "VALUES (%s, %s);", (row['FirstName'], row['LastName']))
            db.commit()

            studId = mycursor.lastrowid

            # StudentAddress db
            mycursor.execute("INSERT INTO StudentAddress(StudentId, Street, City, ZipCode) "
                             "VALUES (%s, %s, %s, %s);", (studId, row['Street'], row['City'], row['Zip']))
            db.commit()

            # StudentBirthday db
            mycursor.execute("INSERT INTO StudentBirthday(StudentId, Month, Day, Year) "
                             "VALUES (%s, %s, %s, %s);", (studId, row['Month'], row['Day'], row['Year']))
            db.commit()

            # AdvisorName db
            mycursor.execute("INSERT INTO AdvisorName(StudentId, AdvisorFirstName, AdvisorLastName) "
                             "VALUES (%s, %s, %s);", (studId, row['AdvisorFirstName'], row['AdvisorLastName']))
            db.commit()

            advId = mycursor.lastrowid

            # StudentAdvisor db
            mycursor.execute("INSERT INTO StudentAdvisor(StudentId, AdvisorId) "
                             "VALUES (%s, %s);", (studId, advId))
            db.commit()

    print("Import data successfully")


# ==================================================================
# main
generateData()
importData()
