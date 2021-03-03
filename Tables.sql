/*database creation*/
create database smartmart;

/*use database*/
use smartmart;

/*create login table and inserted values*/ 
create table login(username varchar(20), password varchar(20));
insert into login values('username','username');
insert into login values('login','login');

/*create products table*/ 
create table products(prodnum varchar(20) primary key, prodname varchar(20), proddesc varchar(1000), prodpric decimal(10,2));

/*create inventory table*/
create table inventory(invid varchar(20), prodnum varchar(20), produnits int, prodwholpric decimal(10,2), prodexpdate date, constraint pk_inv primary key(invid,prodnum), constraint fk_inv foreign key(prodnum) references products(prodnum));

/*create billingdetails table*/
create table billingdetails(billid varchar(20),sno int, prodnum varchar(20),units int, amount decimal(10,2),
constraint pk_billdetails primary key(billid,sno), constraint fk_billdetails foreign key(prodnum) references 
inventory(prodnum));

/*create billing table*/
create table billing(billid varchar(20) primary key, billdate date, subtotal decimal(10,2), taxamount decimal(10,2), total decimal(10,2),
constraint fk_bill foreign key(billid) references billingdetails(billid));
