<?php

$name = $_POST['name'];
/*
if(strlen($name)>0)
{
   $con = mysql_connect("localhost:/tmp/mysql.sock","root","sct");
   if (!$con){
     die('Could not connect: ' . mysql_error());
   }

   mysql_select_db("sct", $con);

   $sqlCmd = sprintf("INSERT INTO Customer (name) 
     VALUES ('%s')", 
      mysql_real_escape_string($name)
	);

   mysql_query($sqlCmd);
   mysql_close($con);
 }*/
// tell python app location
$status_arr = array (
	"status" => "blend-selection.html"
	);

chdir("/Users/kperko/work/sct/www/data/");
$status_json = json_encode($status_arr);
$myFile = "page_location.json";

$fh = fopen($myFile, 'w') or die("can't open file");
fwrite($fh, $status_json);
fclose($fh);

// specify desired url

$blend_url = str_replace(" ", "+", $name);
$url = '/~kperko/html/blend-selection.html?name='. $name;
header( "Location: $url" );

 ?>