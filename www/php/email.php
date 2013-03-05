<?php
require_once 'Swift-4.3.0/lib/swift_required.php';

date_default_timezone_set('America/Los_Angeles');
$today = date("Y-m-d H:i:s");
$customer_email = $_POST['email'];

   $con = mysql_connect("localhost:/tmp/mysql.sock","root","sct");
   if (!$con){
     die('Could not connect: ' . mysql_error());
	}	

	mysql_select_db("sct", $con);

	$getOrderId = sprintf("Select order_id from Orders order by time_created desc limit 1");
	
	$result = mysql_query($getOrderId);
	$row = mysql_fetch_row($result);
	$order_id = $row[0];

	$getCustomerInfo = sprintf("Select customer_id,name,blend_name,
	grinder0_pct,grinder1_pct,grinder2_pct
	 from Orders o join Customer c using(customer_id) join Blend using(blend_id) where order_id=" . $order_id . " order by o.time_created desc limit 1");
	
	$result = mysql_query($getCustomerInfo);
	$row = mysql_fetch_row($result);
	$customer_id = $row[0];
	$customer_name = $row[1];
	$blend_name = $row[2];

   $sqlCmd = sprintf("INSERT INTO Customer (customer_id, email) 
     VALUES (%d,'%s') ON DUPLICATE KEY UPDATE email=VALUES(email)", 
      $customer_id,
      mysql_real_escape_string($customer_email)
	);

   mysql_query($sqlCmd);
   mysql_close($con);

  //setup email
  $to = $customer_email;
  $subject = 'Hey ';
  $subject.= $customer_name ;
  $subject.= ', Thanks for Blending with Us @ Stanford!';
  $msg = 'Thanks for trying the Build a Brew platform by Smart Coffee Technology. 
You made a personalized cup of the ';
  $msg.= $blend_name;
  $msg.= '. Please visit our website to learn more about SCT: smartcoffeetech.com.

<p>We\'re continually improving our system to optimize the customer experience, 
so if you have any feedback please contact us by replying to this email.</p>
 
<p>We appreciate your participation in our demo and hope you enjoyed your coffee.
You can like our Facebook page, link, or follow us on twitter @BuildaBrew. 
We will contact you about future demos in your area. </p>
			<br>
Have a caffeinated day!<br>
			
Kevin and Erik';


  $intro = $customer_name;
  $intro.= ', <br /> Thanks for trying the Build a Brew platform by Smart Coffee Technology. You made a personalized cup of the ';
  $intro.= $blend_name;
  $intro.='.';

  $headers  = 'From: BuildaBrew@SmartCoffeeTech.com';
/*
// swift
// Create the message
$message = Swift_Message::newInstance()
  ->setSubject($subject)
  ->setFrom(array('BuildaBrew@SmartCoffeeTech.com' => 'Smart Coffee Technology'))
  ->setTo(array($customer_email => $customer_name))
  // ->setBody($msg)
  ->setBody($msg)
  // ->addPart('<q>Here is the message itself</q>', 'text/html')
  // ->attach(Swift_Attachment::fromPath('my-document.pdf'))
  ->attach(Swift_Attachment::fromPath('brewing.jpg')->setDisposition('inline'))
  ;*/

$message = Swift_Message::newInstance()
  ->setSubject($subject)
  ->setFrom(array('BuildaBrew@SmartCoffeeTech.com' => 'Smart Coffee Technology'))
  ->setTo(array($customer_email => $customer_name));
$header = $message->embed(Swift_Image::fromPath('coffee-bean-banner.jpg'));
$footer = $message->embed(Swift_Image::fromPath('smartcoffeetechlogo6.png'));
/*$message->setBody(
'<html>' .
' <head><style> div {background-color:brown;}</style></head>' .
' <body>' .
'<div class="emailbox">' .
'  <img height="250" width="550" src="' . $header . '" alt="Image" />' .
$msg .
'  <img src="' . $footer . '" alt="Image" />' .
' </div> </body>' .
'</html>',
  'text/html' // Mark the content-type as HTML
);*/

$message->setBody(
'<html>' .
'<head>' .
'<style>' . 
'div {
	background-color:goldenrod;
	width:600px;
}

.bodytext {
	width:550px;
	padding:25px;
}' .

'</style>' .
	'</head>' .
'<body>' .
'<div class="emailbox" style="background-color:goldenrod;width:600px">' .
'<img height="100" width="600" src="'. $header .'" alt="Image" />' .
'<div class="bodytext" style="background-color:goldenrod;width:550px;padding:25px;">' .
$intro .
'<p> Please visit our website to learn more about SCT: <a href="http://www.smartcoffeetech.com"> smartcoffeetech.com</a>' .
'</p>' .

'<p> We\'re continually improving our system to optimize the customer experience, 
so if you have any feedback please contact us by replying to this email.</p>' .
 
'<p>' . 
'We appreciate your participation in our demo and hope you enjoyed your coffee.
You can like our ' . 
'<a href="https://www.facebook.com/smartcoffeetech">Facebook</a> page ' . 
'or follow us on twitter' . 
'<a href="https://twitter.com/buildabrew">@BuildaBrew</a>.' . 
'We will contact you about future demos in your area. </p>' .
			
'Have a caffeinated day!' .
'<br />' . 
'<br /> Kevin and Erik' .
'</div>' .
'<img height="140" style="padding:20px;" src="'. $footer .'" alt="Image" />' .
'</div>' . 
'</body>' .
'</html>',
'text/html'
);
// Create the Transport
$transport = Swift_SmtpTransport::newInstance('mail.smartcoffeetech.com', 465, 'ssl')
  ->setUsername('info@smartcoffeetech.com')
  ->setPassword('qqABqmvkZhUyCjGlNebD')
  ;

$mailer = Swift_Mailer::newInstance($transport);

// Send the message
$result = $mailer->send($message);

$url = 'twitter.html';
header( "Location: $url");
?>