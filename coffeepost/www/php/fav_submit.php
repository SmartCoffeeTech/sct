<?php 
// set the default tz
date_default_timezone_set('America/Los_Angeles');

//error config settings
ini_set(‘display_errors’, true);
ini_set(‘display_startup_errors’, true);
error_reporting (E_ALL);

// request the form data
$coffee_id = $_POST["coffee_id"];

$epoch_time = date("YmdHis");

/* for testing
$epoch_time = 20130507152500;
$coffee_id = 52; */

exec("echo . | python ../../py/coffee_recommendation_generator.py -id $coffee_id -t $epoch_time");

sleep(.11);

$filename = "/tmp/recinfo$epoch_time";

$handle = fopen($filename, "r");
$data = fread($handle,20);

$data_split = explode(",", $data);

$coffee_id = str_replace("[","",$data_split[0]);
$time_epoch = str_replace(" ","",str_replace("]","",$data_split[1]));

fclose($handle);

if ($epoch_time==$time_epoch){
	$url = 'http://localhost/~kperko/cpost/recommendation.html?usr=' . $time_epoch;
	header( "Location: $url" );
}

?>