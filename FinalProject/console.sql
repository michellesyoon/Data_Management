# Normalized Tables
create table Professor(
    ProfessorId int primary key auto_increment,
    FirstName varchar(50) NOT NULL,
    LastName varchar(50) NOT NULL
);

create table Subject(
    SubjectId int primary key auto_increment,
    SubjectName varchar(50) NOT NULL
);

create table Course(
    CourseId int primary key auto_increment,
    ProfessorId int,
    SubjectId int,
    CourseName varchar(50) NOT NULL,
    FOREIGN KEY CourseProfId(ProfessorId) references Professor(ProfessorId),
    FOREIGN KEY CourseSubId(SubjectId) references Subject(SubjectId)
);

create table User(
    UserId int primary key auto_increment,
    UserEmail varchar(50) NOT NULL,
    DeletedUser tinyint
);

create table Rate(
    RateId int primary key auto_increment,
    ProfessorId int,
    SubjectId int,
    CourseId int,
    UserId int,
    RateNumber float,
    UserComment varchar(200) NOT NULL,
    FOREIGN KEY RateProfId(ProfessorId) references Professor(ProfessorId),
    FOREIGN KEY RateSubId(SubjectId) references Subject(SubjectId),
    FOREIGN KEY RateCourseId(CourseId) references Course(CourseId),
    FOREIGN KEY RateUserId(UserId) references User(UserId)
);

# Indexes
create index Professor_FirstName_index
	on Professor (FirstName);

create index Professor_LastName_index
	on Professor (LastName);

create index Subject_SubjectName_index
	on Subject (SubjectName);

create index Course_CourseName_index
	on Course (CourseName);

create index Rate_RateNumber_index
	on Rate (RateNumber);

create index Rate_UserComment_index
	on Rate (UserComment);

# Store Procedure
create procedure getAllRecords()
begin
    select Professor.ProfessorId, FirstName, LastName, SubjectName, CourseName, User.UserId,
           UserEmail, RateNumber, UserComment, DeletedUser
    from Rate
    join Professor ON Rate.ProfessorId = Professor.ProfessorId
    join Subject ON Rate.SubjectId = Subject.SubjectId
    join Course ON Rate.CourseId = Course.CourseId
    join User ON Rate.UserId = User.UserId
    where DeletedUser = 0
    order by LastName asc;
end;

call getAllRecords();

# Database View
CREATE VIEW vProfessorInfo as
    select Professor.ProfessorId, FirstName, LastName, SubjectName, CourseName, User.UserId,
           UserEmail, RateNumber, UserComment, DeletedUser
    from Rate
    join Professor ON Rate.ProfessorId = Professor.ProfessorId
    join Subject ON Rate.SubjectId = Subject.SubjectId
    join Course ON Rate.CourseId = Course.CourseId
    join User ON Rate.UserId = User.UserId
    where DeletedUser = 0
    order by LastName asc;
