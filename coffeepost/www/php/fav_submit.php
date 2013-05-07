<?php 
// set the default tz
date_default_timezone_set('America/Los_Angeles');


// request the form data
$coffee_id = $_POST["coffee_id"];
$epoch_time = date("YmdHis");

exec("echo . | python scripter.py -id $coffee_id -t $epoch_time");

?>