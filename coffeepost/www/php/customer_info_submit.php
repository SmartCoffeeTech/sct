<?php
// setup connection with database
// add full dir path
include("/db_config.php");

// get from query string
$customer_id = $_POST["customer_id"];

$customer_name = $_POST["customer_name"];
$customer_city = $_POST["customer_city"];
$customer_address = $_POST["customer_address"];
$customer_state = $_POST["customer_state"];
$customer_zip = $_POST["customer_zip"];

if ($customer_name && $customer_city && $customer_address && $customer_state && $customer_zip)
{
	// update this to use a production ready config file
	// $con = mysql_connect(db_host,db_user,db_pass);
	$con = mysql_connect("localhost:/tmp/mysql.sock","root","sct");
	if (!$con){
	die('Could not connect: ' . mysql_error());
	}

	mysql_select_db("sct", $con);

	// record customer selection into db
	// not an "order" until the put in their address? just a customer_rec?
	// only one order per customer during trial period. 

	$sqlCmd = sprintf("INSERT IGNORE INTO Customer (customer_id,customer_name, city, address, state, zip, shipping_info_submitted) VALUES(%d, %s,%s,%s,%s,%s,1)
	ON DUPLICATE KEY UPDATE customer_name=VALUES(customer_name),customer_city=VALUES(customer_city),customer_address=VALUES(customer_address),
	customer_state=VALUES(customer_state),customer_zip=VALUES(customer_zip), shipping_info_submitted=VALUES(shipping_info_submitted))", 
	$customer_id,
	mysql_real_escape_string($customer_name),
	mysql_real_escape_string($customer_city),
	mysql_real_escape_string($customer_address),
	mysql_real_escape_string($customer_state),
	mysql_real_escape_string($customer_zip)
	);

	mysql_query($sqlCmd);
	mysql_close($con);

	// redirect to another url
	$url = '/customer-order-complete.html';
	header( "Location: $url" );

}

?>