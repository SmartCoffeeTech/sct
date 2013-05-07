<?php 
// set the default tz
date_default_timezone_set('America/Los_Angeles');


// request the form data
$coffee_id = $_POST["coffee_id"];
$epoch_time = date("YmdHis");

exec("echo . | python ../../py/coffee_recommendation_generator.py -id $coffee_id -t $epoch_time");

?>