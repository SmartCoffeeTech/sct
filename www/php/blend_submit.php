<?php

// gets data from ?.html
$customization_pct = $_POST['customization'];
$name_blend = $_POST['blend'];

date_default_timezone_set('America/Los_Angeles');
$today = date("Y-m-d H:i:s");

if(strlen($customization_pct)>0)
{
   $con = mysql_connect("localhost:/tmp/mysql.sock","root","sct");
   if (!$con){
     die('Could not connect: ' . mysql_error());
   }

	mysql_select_db("sct", $con);

	$getOrderId = sprintf("Select order_id from Orders order by time_created desc limit 1");

	$result = mysql_query($getOrderId);
	$row = mysql_fetch_row($result);
	$order_id = $row[0];

   $sqlCmd = sprintf("INSERT INTO Orders (order_id, customization_pct) 
     VALUES (%d,%d) ON DUPLICATE KEY UPDATE customization_pct=VALUES(customization_pct)", 
      $order_id,
      $customization_pct
	);

   mysql_query($sqlCmd);
   mysql_close($con);
 }

// tell python user location app
$status_arr = array (
	"status" => "grinding.html"
	);

chdir("/Users/kperko/work/sct/www/data/");
$status_json = json_encode($status_arr);
$myFile = "page_location.json";

$fh = fopen($myFile, 'w') or die("can't open file");
fwrite($fh, $status_json);
fclose($fh);

// specify desired url

$blend_url = str_replace(" ", "+", $url_blend);
$url = '/~kperko/html/grinding.html';
header( "Location: $url" );
 ?>