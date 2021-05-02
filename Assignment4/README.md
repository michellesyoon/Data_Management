# Assignment4

Name: Michelle Yoon
Student Id: 2356544
Course: CPSC 408

For the majority of this assignment, I referred back to our class zoom lecture on April 8th,2021.

The 5 normalized databases created were StudentName, StudentAddress, StudentBirthday, AdvisorName, and StudentAdvisor

In addition, for the code below, to create the csv file, the user must type the filename with .csv, ex: filename.csv as one string.
If the user does not follow that rule, I created a check statement for it.

*filename = input("Enter a filename (ex: filename.csv): ")*

*if not filename.__contains__(".csv"):
   print("Error: Enter invalid filename")
   print("Exiting...")
   quit()*
   
   
## UPDATE! PLEASE  READ THIS BEFORE RUNNING MY CODE
## In my generating data function, when it asks you to enter the the filename, please type mydata.csv. I just realized that for my import data function I hard coded 'mydata.csv' and that is the file where it will to import the generated data. I am so sorry about this! 
 
 Resources: <br>
 Faker Library: https://www.geeksforgeeks.org/python-faker-library/ <br>
 String-substring: https://www.pythonpool.com/python-substring/#:~:text=Table%20Containing%20all%20Python%20String%20Methods%20%20,of%20a%20substring%20%2034%20more%20rows%20
