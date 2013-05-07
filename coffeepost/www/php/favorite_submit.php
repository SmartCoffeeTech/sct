<?php
ini_set('display_errors', 1);
$fav_coffee = $_POST['fav_coffee'];
$coffee_id = $_POST['coffee_id'];
echo " Coffee Name: ";
echo $fav_coffee;
echo "   Coffee ID: ";
echo $coffee_id;
//specify desired url
/*header( "Location: ../recommendation.html" );*/
?>