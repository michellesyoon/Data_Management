create table StudentName(
    StudentId int primary key auto_increment,
    FirstName varchar(50) NOT NULL,
    LastName varchar(50) NOT NULL
);

create table StudentAddress(
    AddressId int primary key auto_increment,
    StudentId int,
    Street varchar(50),
    City varchar(50),
    Zipcode char(5),
    FOREIGN KEY StudentAddress(StudentId) references StudentName(StudentId)
);


create table StudentJob(
    StudentJobId int primary key auto_increment,
    StudentId int,
    Job varchar(50),
    FOREIGN KEY StudentJob(StudentId) references StudentName(StudentId)

);

create table StudentBirthday(
    StudentBirthdayId int primary key auto_increment,
    StudentId int,
    Month int,
    Day int,
    Year int,
    FOREIGN KEY StudentBirthday(StudentId) references StudentName(StudentId)
);

create table AdvisorName(
    AdvisorId int primary key auto_increment,
    StudentId int,
    AdvisorFirstName varchar(50),
    AdvisorLastName varchar(50),
    FOREIGN KEY Advisor(StudentId) references StudentName(StudentId)
);


create table StudentAdvisor(
    StudentAdvisorId int primary key auto_increment,
    StudentId int,
    AdvisorId int,
    FOREIGN KEY StudentAdvisor(AdvisorId) references AdvisorName(AdvisorId)
);

