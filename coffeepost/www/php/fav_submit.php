<?php 
// set the default tz
date_default_timezone_set('America/Los_Angeles');

// request the form data
$coffee_id = $_POST["coffee_id"];
$epoch_time = date("YmdHis");

/* for testing
$epoch_time = 20130507152500;
$coffee_id = 52; */

$output = exec("python ../../py/coffee_recommendation_generator.py -id $coffee_id -t $epoch_time");

$filename = "/tmp/recinfo$epoch_time";

$handle = fopen($filename, "r");
$data = fread($handle,27);

$data_split = explode(",", $data);

$coffee_id = str_replace("[","",$data_split[0]);
$time_epoch = str_replace(" ","",str_replace("]","",$data_split[1]));
$cid = str_replace("'","", str_replace(" ","",str_replace("]","",$data_split[2])));

fclose($handle);

if ($epoch_time==$time_epoch){
	$URL_Base = 'http://localhost/~kperko/cpost/';
	$url =  $URL_Base . 'recommendation.html?usr=' . $time_epoch;
	header( "Location: $url" );
}

?>