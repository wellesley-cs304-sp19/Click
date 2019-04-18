USE `clickdb`;

/*user table
holds user's contact information*/
Drop table if exists apply;
Drop table if exists hasSkill;
drop table if exists user;
create table user(
    email varchar(50),
    password varchar(50),
    name varchar(50),
    active enum('yes','no'),
    userType enum('alum','resident','student'),
    primary key (email)
    );

/*project table
projects that students can apply to and alum/residents can post*/
Drop table if exists requires;
drop table if exists project;
create table project(
	pid int auto_increment,
	name varchar(50),
	minHours int,
	pay float,
	location enum('local','remote'),
	primary key (pid)
	);

/*skills table
all possible skills*/
Drop table if exists skills;
Create table skills(
    sid int auto_increment,
    skill varchar(30),
    primary key (sid));

/*requires table
projects can requires skills*/
Create table requires(
    pid int,
    sid int,
    primary key (pid, sid),
    foreign key (pid) references project(pid) on delete cascade,
    foreign key (sid) references skills(sid) on delete cascade
    );

/*hasSkill table
relates students to skills*/   
Create table hasSkill(
    email varchar(50),
    sid int,
    primary key (email, sid),
    foreign key (email) references user(email) on delete cascade,
    foreign key (sid) references skills(sid) on delete cascade
    );

/*apply table
relates a student to a project*/
Create table apply(
    email varchar(50),
    pid int,
    primary key (email, pid),
    foreign key (email) references user(email) on delete cascade,
    foreign key (pid) references project(pid) on delete cascade
    );