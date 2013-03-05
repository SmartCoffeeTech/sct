drop table if exists Customer;
create table Customer (
	customer_id int auto_increment,
	customer_name varchar(255),
	customer_email varchar(255),
	time_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	modified timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	primary key(customer_id)
	);
	
create table Blend (
	row_id int auto_increment,
	blend_id int,	
	blend_name text,
	coffee_id int,
	coffee_pct int,
	time_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	primary key(row_id),
	unique key(blend_id,coffee_id)
);


INSERT INTO Blend (blend_id,blend_name,coffee_id,coffee_pct) VALUES(1,'Golden Gate',1,25);
INSERT INTO Blend (blend_id,blend_name,coffee_id,coffee_pct) VALUES(1,'Golden Gate',2,25);
INSERT INTO Blend (blend_id,blend_name,coffee_id,coffee_pct) VALUES(1,'Golden Gate',3,50);
INSERT INTO Blend (blend_id,blend_name,coffee_id,coffee_pct) VALUES(2,'Stanford Cardinal',1,10);
INSERT INTO Blend (blend_id,blend_name,coffee_id,coffee_pct) VALUES(2,'Stanford Cardinal',2,50);
INSERT INTO Blend (blend_id,blend_name,coffee_id,coffee_pct) VALUES(2,'Stanford Cardinal',3,40);
INSERT INTO Blend (blend_id,blend_name,coffee_id,coffee_pct) VALUES(3,'Fog City',1,50);
INSERT INTO Blend (blend_id,blend_name,coffee_id,coffee_pct) VALUES(3,'Fog City',2,50);
INSERT INTO Blend (blend_id,blend_name,coffee_id,coffee_pct) VALUES(3,'Fog City',3,0);
INSERT INTO Blend (blend_id,blend_name) VALUES(4,'Custom Creation');
INSERT INTO Blend (blend_id,blend_name,coffee_id,coffee_pct) VALUES(6,'Indonesian',1,100);
INSERT INTO Blend (blend_id,blend_name,coffee_id,coffee_pct) VALUES(5,'Ethiopian',2,100);
INSERT INTO Blend (blend_id,blend_name,coffee_id,coffee_pct) VALUES(7,'Colombian',3,100);

drop table if exists Coffee;
create table Coffee (
	coffee_id int auto_increment,
	coffee_name varchar(255) default NULL,
	roast_date timestamp DEFAULT '00-00-00 00:00:00',
	roast_company varchar(255),
	country_of_origin varchar(255),
	region varchar(200),
	farm varchar(200),
	varietal varchar(200),
	processing_method varchar(200),
	altitude varchar(200),
	grinder varchar(255),
	time_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	primary Key(coffee_id)
);

INSERT INTO Coffee (coffee_name,roast_date,roast_company,country_of_origin,region,farm,varietal,processing_method,altitude,grinder)
 VALUES ('','2013-02-14','Sightglass','Indonesia','Sulawesi','Toarco','Typica','Washed','1400-2000','2');
INSERT INTO Coffee (coffee_name,roast_date,roast_company,country_of_origin,region,farm,varietal,processing_method,altitude,grinder)
 VALUES ('','2013-02-20','Fourbarrel','Ethiopia','Yukro','Agaro','Heirloom','Washed','1900-2100','0');
INSERT INTO Coffee (coffee_name,roast_date,roast_company,country_of_origin,region,farm,varietal,processing_method,altitude,grinder)
 VALUES ('Los Gigantes','2013-02-19','Ritual','Colombia','Huila','Desarrollo','Caturra','Washed','1500-1900','1');

drop table if exists Grinder;
create table Grinder (
	row_id int auto_increment,
	grinder_name varchar(1),
	coffee_id int,
	time_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	primary key(row_id)
);

drop table if exists Orders;
create table Orders (
	order_id int auto_increment,
	customer_id int,
	blend_id int,
	grinder0_pct decimal(8,5) unsigned default NULL,
	grinder1_pct decimal(8,5) unsigned default NULL,
	grinder2_pct decimal(8,5) unsigned default NULL,
	grind_complete timestamp DEFAULT '00-00-00 00:00:00',
	time_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	primary key(order_id)
);

INSERT INTO Orders (customer_id,blend_id,coffee_id,grinder0_pct,grinder1_pct,grinder2_pct,grind_complete,time_created)
VALUES ((Select customer_id from Customer where name='Kevin' order by time_created desc limit 1),2,NULL,40,20,40,'readyToBrew','blendSelection');
	
	
	
drop table if exists Cafe;
create table Cafe (
	cafe_id int auto_increment,
	cafe_name varchar(255),
	address varchar(255),
	city varchar(255),
	state char(2),
	country char(2),
	time_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	primary key(cafe_id))

INSERT INTO Cafe (cafe_name,address,city,state,country) VALUES ('BuildaBrew','','Palo Alto','CA','US');
	
 
	
