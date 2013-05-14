<?php

    define('CONTACT_FORM_TO_NAME','Orders');
    define('CONTACT_FORM_TO_EMAIL','info@smartcoffeetech.com');
	
    define('CONTACT_FORM_SMTP_HOST','mail.smartcoffeetech.com');
    define('CONTACT_FORM_SMTP_USER','info@smartcoffeetech.com');
	define('CONTACT_FORM_SMTP_PORT','26');
	define('CONTACT_FORM_SMTP_SECURE','ssl');
    define('CONTACT_FORM_SMTP_PASSWORD','qqABqmvkZhUyCjGlNebD');
	
    define('CONTACT_FORM_SUBJECT','Incoming Order');

    define('CONTACT_FORM_MSG_INVALID_DATA_NAME','Enter Your Name');
    define('CONTACT_FORM_MSG_INVALID_DATA_NUMBER','Enter Phone Number');
	define('CONTACT_FORM_MSG_INVALID_DATA_MAIL','Enter Valid Email Address');
    define('CONTACT_FORM_MSG_INVALID_DATA_MESSAGE','No Delivery Address');
    define('CONTACT_FORM_MSG_INVALID_DATA_STREET','Enter Street Address');
    define('CONTACT_FORM_MSG_INVALID_DATA_CITY','Enter City');
    define('CONTACT_FORM_MSG_INVALID_DATA_STATE','Enter State');
    define('CONTACT_FORM_MSG_INVALID_DATA_ZIP','Enter Zip Code');
	
    define('CONTACT_FORM_SEND_MSG_OK','Thank you for your Order.');
    define('CONTACT_FORM_SEND_MSG_ERROR','Sorry, we can\'t send this message. Please try again.');

	// db config params
	define('DB_CON', "localhost:/tmp/mysql.sock");
	define('DB_USER', "root");
	define('DB_PWD', "sct");
	define('DB_SCHEMA', "coffeehouse");
    
?>