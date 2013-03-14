<?php

if(isset($_POST['submit']))
{
   $con = mysql_connect("localhost:/tmp/mysql.sock","root","sct");
   if (!$con){
     die('Could not connect: ' . mysql_error());
   }

   mysql_select_db("sct", $con);

   $sqlCmd = sprintf("INSERT INTO Customer (name, blend_name, email) 
     VALUES ('%s','%s','%s')", 
      mysql_real_escape_string($_POST["name"]),
      mysql_real_escape_string($_POST["blendName"]),
      mysql_real_escape_string($_POST["email"])
	);

   mysql_query($sqlCmd);
   mysql_close($con);
 }
// specify desired url
$url = 'www.google.com';
header( "Location: $url" );
 ?>