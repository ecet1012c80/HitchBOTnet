drop table if exists entries;
create table entries(
	id integer primary key autoincrement,
	timestamp datetime DEFAULT CURRENT_TIMESTAMP not null,
	latitude int not null,
	longitude int not null,
	gpsaccuracy int,
	battery int,
	temperature int,
	lastwake datetime
);