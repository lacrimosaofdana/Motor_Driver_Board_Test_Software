-- Motor Driver Board Test Software
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

drop database if exists test;
create database if not exists test;
use test;
-- -----------------------------------------------
-- table structures
-- -----------------------------------------------

create table results (
id varchar(40) not null,
ecurrent float not null,
voltage float not null,
epower float not null,
rev float not null,
validate bool not null,
test_user varchar(20),
test_console varchar(20),
test_time datetime,
primary key (id)
) engine = innodb;


create table Users (
id INTEGER AUTO_INCREMENT,
username varchar(20),
password_hash varchar(128),
admin_status bool,
primary key (id)
) engine = innodb;

create table configuration (
id integer not null,
al float,
ah float,
vl float,
vh float,
wl float,
wh float,
tl float,
th float,
primary key (id)
) engine = innodb;


insert into results values
('23454', 5, 12, 20, 24, True, 'pzheng46', 'Console 1', '2023-05-28 11:50:36');

insert into configuration values
(1, 1, 2, 1, 2, 1, 2, 1, 2);
