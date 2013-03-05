<?php

$name = $_POST['name'];

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
 }
// specify desired url
$blend_url = str_replace(" ", "+", $name);
$url = 'blend-menu.html?name='. $name;
header( "Location: $url" );

 ?>