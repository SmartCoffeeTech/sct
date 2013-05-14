CREATE TABLE Orders (
  order_id int(11) NOT NULL AUTO_INCREMENT,
  customer_id int(11) NOT NULL,
  coffee_id int(11) NOT NULL,
  # only works on mysql 5.6.x+
  # time_created datetime DEFAULT CURRENT_TIMESTAMP,
  # time_modified datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  # for compatability with mysql 5.5
  time_created timestamp DEFAULT '00-00-00 00:00:00',
  time_modified timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (order_id)
) ENGINE=InnoDB;