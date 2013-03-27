<?php
$order_blend_name = $_POST['order_blend_name'];
$customer_prefs_arr = $_POST['customer_prefs_arr'];

$base_prefs_arr = array (
	"acidity" => 0,
	"body" => 0,  
	"chocolatey" => 0,
	"earthy" => 0, 
	"floral" => 0,
	"fruity" => 0,
	"herby" => 0,
	"nutty" => 0,
	"smokey" => 0,
	"spicy" => 0,
	"winey" => 0
	);

# if length > 0
if (count($customer_prefs_arr)>0){
	ksort($customer_prefs_arr);
}

foreach ($customer_prefs_arr as $key => $val) {
    // echo "$key = $val\n";
    
	if ($key=='acidity'){
		$base_prefs_arr[$key]=floatval($val);
	}
	elseif ($key=='body'){
		$base_prefs_arr[$key]=floatval($val);
	}
	elseif ($key=='chocolatey'){
		$base_prefs_arr[$key]=floatval($val);
	}
	elseif ($key=='earthy'){
		$base_prefs_arr[$key]=floatval($val);
	}
	elseif ($key=='floral'){
		$base_prefs_arr[$key]=floatval($val);
	}
	elseif ($key=='fruity'){
		$base_prefs_arr[$key]=floatval($val);
	}
	elseif ($key=='herby'){
		$base_prefs_arr[$key]=floatval($val);
	}
	elseif ($key=='nutty'){
		$base_prefs_arr[$key]=floatval($val);
	}
	elseif ($key=='smokey'){
		$base_prefs_arr[$key]=floatval($val);
	}
	elseif ($key=='spicy'){
		$base_prefs_arr[$key]=floatval($val);
	}
	elseif ($key=='winey'){
		$base_prefs_arr[$key]=floatval($val);
	}
};

/*
foreach ($base_prefs_arr as $key => $val) {
    echo "$key = $val\n";
};*/
	

$base_prefs_json = json_encode($base_prefs_arr);

if(count($customer_prefs_arr)>0)
{
   $con = mysql_connect("localhost:/tmp/mysql.sock","root","sct");
   if (!$con){
     die('Could not connect: ' . mysql_error());
	}

	mysql_select_db("sct", $con);
	
	$getCustomerId = sprintf("Select customer_id,name from Customer order by time_created desc limit 1");
	
	$result = mysql_query($getCustomerId);
	$row = mysql_fetch_row($result);
	$customer_id = $row[0];
	$customer_name = $row[1];

   $sqlCmd = sprintf("INSERT INTO Orders (customer_id, taste_profile, order_blend_name) 
     VALUES (%d,'%s','%s')", 
      $customer_id,
      $base_prefs_json,
	  $order_blend_name
	);

   mysql_query($sqlCmd);
   mysql_close($con);
 }

// update the application state for python
$status_arr = array (
	"status" => "base-blend.html"
	);

chdir("/Users/kperko/work/sct/www/data/");
$status_json = json_encode($status_arr);
$myFile = "page_location.json";

$fh = fopen($myFile, 'w') or die("can't open file");
fwrite($fh, $status_json);
fclose($fh);
// redirect the user to the next page
$blend_url = str_replace(" ", "+", $name);
$url = '/~kperko/html/base-blend.html?name='. $customer_name;
header( "Location: $url" );
?>