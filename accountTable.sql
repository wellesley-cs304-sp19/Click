/*new table for just for username and table--Gabby Liu*/

use clickdb;

drop table if exists account;

create table account(
    username varchar(50) not null primary key,
    hashed char(60)
);