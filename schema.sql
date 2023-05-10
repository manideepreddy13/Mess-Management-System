create table Mess_Details(
    Mess_Id integer PRIMARY KEY,
    Mess_Name varchar(30),
    Allocated integer,
    Capacity integer
);

create table Mess_Manager(
    Manager_Id varchar(9) PRIMARY KEY,
    Manager_Name varchar(40),
    Mess_Id integer,
    foreign key (Mess_Id) references Mess_Details(Mess_Id) on update cascade on delete cascade
);

create table Student(
    Student_Name varchar(50) NOT NULL,
    Roll_No varchar(9) PRIMARY KEY,
    email varchar(50) NOT NULL,
    Mess_Id integer,
    Hostel_Id integer,
    Ref_Id varchar(20),
    foreign key (Hostel_Id) references Hostel_Details(Hostel_Id) on update cascade on delete cascade,
    foreign key (Mess_Id) references Mess_Details(Mess_Id) on update cascade on delete cascade
);

CREATE TABLE Hostel_Warden (
	Warden_Id varchar(9) PRIMARY KEY,
	Warden_Name varchar(50),
	Hostel_Id integer,
        foreign key (Hostel_Id) references Hostel_Details(Hostel_Id) on update cascade on delete cascade
);

CREATE TABLE Hostel_Details(
	Hostel_Id integer NOT NULL PRIMARY KEY,
	Hostel_Name varchar(30) NOT NULL
);

CREATE TABLE Login_Creds(
    LC_Name varchar(30) NOT NULL,
	Username varchar(20) NOT NULL PRIMARY KEY,
	Passcode varchar(30) NOT NULL UNIQUE
);