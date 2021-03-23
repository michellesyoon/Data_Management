# Assignment3 

Name: Michelle Yoon
Course: CPSC 408

Resources:
https://thispointer.com/python-pandas-how-to-display-full-dataframe-i-e-print-all-rows-columns-without-truncation/
to display all columns and rows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

https://www.w3schools.com/python/pandas/pandas_dataframes.asp
myCursor.execute("SELECT * FROM Student")
StudentTable = myCursor.fetchall()
df = pd.read_csv("./students.csv")

if not StudentTable:
    for i in StudentTable:
        myCursor.execute("UPDATE Student SET isDeleted = 0")

    df.to_sql("Student", conn, if_exists='append', index=False)
