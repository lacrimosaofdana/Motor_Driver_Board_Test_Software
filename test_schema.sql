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


create table modbus_data (
id integer not null,
port_data varchar(40),
baudrate float,
bytesize int,
parity varchar(20),
stopbits int,
address int,
count int,
slave_address int,
primary key (id)
) engine = innodb;


insert into results values
('23454', 5, 12, 20, 24, True, 'pzheng46', 'Console 1', '2023-05-28 11:50:36');

insert into configuration values
(1, 1, 2, 1, 2, 1, 2, 1, 2);

insert into modbus_data values
(1, 'COM1', 9600, 8, 'N', 1, 0xB9, 4, 1),
(2, 'COM2', 9600, 8, 'N', 1, 0xB6, 4, 1),
(3, 'COM3', 9600, 8, 'N', 1, 0xBD, 4, 1),
(4, 'COM4', 9600, 8, 'N', 1, 0x62, 4, 1),
(5, 'COM5', 9600, 8, 'N', 1, 0xB9, 4, 1),
(6, 'COM6', 9600, 8, 'N', 1, 0xB6, 4, 1),
(7, 'COM7', 9600, 8, 'N', 1, 0xBD, 4, 1),
(8, 'COM8', 9600, 8, 'N', 1, 0x62, 4, 1);