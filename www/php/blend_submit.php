<?php

$customization_pct = $_POST['customization'];

$name_blend = $_POST['blend'];

date_default_timezone_set('America/Los_Angeles');
$today = date("Y-m-d H:i:s");

// list($name, $blend) = split(',', $name_blend);
// $url_blend = $blend;
/*
if (substr($blend,-5)=='Blend'){
	$blend = substr($blend, 0,strlen($blend)-6);
}
else if (substr($blend,-13)=='Single Origin'){
	$blend = substr($blend, 0,strlen($blend)-14);
}
*/

if(strlen($customization_pct)>0)
{
   $con = mysql_connect("localhost:/tmp/mysql.sock","root","sct");
   if (!$con){
     die('Could not connect: ' . mysql_error());
   }

	mysql_select_db("sct", $con);

	$getCustomerId = sprintf("Select customer_id from Orders order by time_created desc limit 1");

	$result = mysql_query($getCustomerId);
	$row = mysql_fetch_row($result);
	$customer_id = $row[0];

	// $getBlend = sprintf("Select blend_id from Blend where blend_name='" . $blend . "' order by time_created desc limit 1");

	// $result = mysql_query($getBlend);
	// $row = mysql_fetch_row($result);
	// $blend_id = $row[0];

   $sqlCmd = sprintf("INSERT INTO Orders (customer_id, customization_pct) 
     VALUES (%d,%d) ON DUPLICATE KEY UPDATE customization_pct=VALUES(customization_pct)", 
      $customer_id,
      $customization_pct
	);
   echo $sqlCmd;
   mysql_query($sqlCmd);
   mysql_close($con);
 }
// specify desired url
/* $blend_url = str_replace(" ", "+", $url_blend);
$url = 'grinding_blend.html?blend='. $blend_url;
header( "Location: $url" ); */
 ?>