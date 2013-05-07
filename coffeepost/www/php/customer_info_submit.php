<?php
// setup connection with database
// add full dir path
include("/db_config.php");

// get from query string
$customer_id = $_POST["customer_id"];
$customer_id = $customer_id/1003;

$customer_name = $_POST["contact-form-name"];
$customer_city = $_POST["contact-form-mail"];
$customer_address = $_POST["contact-form-street"];
$customer_city = $_POST["contact-form-city"];
$customer_state = $_POST["contact-form-state"];
$customer_zip = $_POST["contact-form-zip"];

if ($customer_name && $customer_city && $customer_address && $customer_city && $customer_state && $customer_zip)
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
	ON DUPLICATE KEY UPDATE name=VALUES(name),city=VALUES(city),address=VALUES(address),
	state=VALUES(state),zip=VALUES(zip), shipping_info_submitted=VALUES(shipping_info_submitted))", 
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