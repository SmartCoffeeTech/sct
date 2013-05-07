<?php

$file = getopt("t:c:");

$customer_id = $file['c'];
$customer_id = $customer_id*1003;

$url = '/~kperko/html/customer-info.html?usr='. $file['t'] . '?detail=' . $customer_id;
header( "Location: $url" );

?>