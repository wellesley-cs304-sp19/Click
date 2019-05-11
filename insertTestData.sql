use clickdb;

insert into user(email,password,name, active, userType) 
values 
("alum1@gmail.com","alum1","Alum One", "yes","alum"),
("resident1@gmail.com","resident1","Resident One", "no","resident"),
("student1@gmail.com","student1","Student One", "yes","student"),
("student2@gmail.com","student2","Student Two", "yes","student");

insert into project(name,minHours,pay,location) 
values 
("interesting",10, 13.5,'local'),
("boring",15,20.0,'local'),
("tough",8,16.8,'remote');


insert into skills(skill) 
values 
("cooking"),
("babysitting"),
("Mandarin tutoring");

insert into requires(pid, sid)
values
(1,1),
(1,3),
(2,2),
(2,1),
(3,3);


insert into hasSkill(email, sid)
values
("student1@gmail.com",1),
("student1@gmail.com",2);


insert into apply(email, pid)
values
("student1@gmail.com",1),
("student1@gmail.com",2),
("student2@gmail.com",1);