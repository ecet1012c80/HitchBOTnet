drop table if exists entries;
create table entries(
	id integer primary key autoincrement,
	recieved datetime DEFAULT CURRENT_TIMESTAMP not null,
	timestamp datetime,
	latitude int not null,
	longitude int not null,
	gpsaccuracy int,
	battery int,
	temperature int,
	lastwake datetime
);

INSERT INTO entries 
(latitude, longitude, gpsaccuracy, battery, temperature, lastwake) 
VALUES (33.9383158, -84.5223048, 5, 90, 30, 'never');