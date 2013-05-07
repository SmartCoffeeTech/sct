create table Customer (
	customer_id int(11) not null auto_increment,
	customer_name varchar(255) default null,
	email varchar(255) default null,
	city varchar(255) default null,
	state varchar(255) default null,
	state_abbrev char(2) default null,
	zip char(5) default null,
	shipping_info_submitted tinyint unsigned default '0',
	time_created DATETIME default CURRENT_TIMESTAMP,
	time_modified DATETIME default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY(customer_id)
);
	
create table Orders (
	order_id int(11) not null auto_increment,
	customer_id int(11) not null,
	coffee_id int(11) not null,
	time_created DATETIME default CURRENT_TIMESTAMP,
	time_modified DATETIME default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	primary key(order_id)
);

-- first we make a recommendation - then we have customer info
-- on rec create a customer id and order
-- fill in information later
-- if we use the same json filename the files will overwrite each other
-- need to use something to identify the customer - their id in the filename? works.
-- js must be aware of their id. 