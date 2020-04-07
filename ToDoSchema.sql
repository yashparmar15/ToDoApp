create table ToDo(
    id integer primary key autoincrement,
    task text not null ,
    descrip text not null
);

create table Doing(
    id integer primary key autoincrement,
    task text not null,
    descrip text not null
);

create table Done(
    id integer primary key autoincrement,
    task text not null,
    descrip text not null
);