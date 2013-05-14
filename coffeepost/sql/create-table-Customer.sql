CREATE TABLE Customer (
  customer_id int(11) NOT NULL AUTO_INCREMENT,
  customer_name varchar(255) DEFAULT NULL,
  email varchar(255) DEFAULT NULL,
  city varchar(255) DEFAULT NULL,
  address varchar(255) DEFAULT NULL,
  state varchar(255) DEFAULT NULL,
  state_abbrev char(2) DEFAULT NULL,
  zip char(5) DEFAULT NULL,
  shipping_info_submitted tinyint(3) unsigned DEFAULT '0',
  time_created timestamp DEFAULT '00-00-00 00:00:00',
  time_modified timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (customer_id)
) ENGINE=InnoDB;