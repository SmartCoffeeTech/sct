<?php

	/**************************************************************************/
	/**************************************************************************/
	date_default_timezone_set('America/Los_Angeles');
	require_once('config.php');
	require_once('../../include/functions.php');
	require_once('../../include/phpMailer/class.phpmailer.php');
	require_once('../../include/class/Template.class.php');
	
	/**************************************************************************/
	
	$response=array('error'=>0,'info'=>null);

	$values=array
	(
		'contact-form-name'						=> $_POST['contact-form-name'],
		'contact-form-mail'						=> $_POST['contact-form-mail'],
		'contact-form-street'					=> $_POST['contact-form-street'],
		'contact-form-city'					    => $_POST['contact-form-city'],
		'contact-form-state'					=> $_POST['contact-form-state'],
		'contact-form-zip'					    => $_POST['contact-form-zip'],
		'contact-form-roast'					=> $_POST['contact-form-roast'],		
		'contact-form-coffee'					=> $_POST['contact-form-coffee'],
	);
	
	/**************************************************************************/
	
	if(isEmpty($values['contact-form-name']))
	{
		$response['error']=1;
		$response['info'][]=array('fieldId'=>'contact-form-name','message'=>CONTACT_FORM_MSG_INVALID_DATA_NAME);
	}

	if(isEmpty($values['contact-form-street']))
	{
		$response['error']=1;
		$response['info'][]=array('fieldId'=>'contact-form-street','message'=>CONTACT_FORM_MSG_INVALID_DATA_STREET);
	}

	if(isEmpty($values['contact-form-city']))
	{
		$response['error']=1;
		$response['info'][]=array('fieldId'=>'contact-form-city','message'=>CONTACT_FORM_MSG_INVALID_DATA_CITY);
	}

	if(isEmpty($values['contact-form-state']))
	{
		$response['error']=1;
		$response['info'][]=array('fieldId'=>'contact-form-state','message'=>CONTACT_FORM_MSG_INVALID_DATA_STATE);
	}

	if(isEmpty($values['contact-form-zip']))
	{
		$response['error']=1;
		$response['info'][]=array('fieldId'=>'contact-form-zip','message'=>CONTACT_FORM_MSG_INVALID_DATA_ZIP);
	}
	
	if(!validateEmail($values['contact-form-mail']))
	{
 		$response['error']=1;	
		$response['info'][]=array('fieldId'=>'contact-form-mail','message'=>CONTACT_FORM_MSG_INVALID_DATA_MAIL);
	}
	
	if($response['error']==1) createResponse($response);
	
	/**************************************************************************/

	if(isGPC()) $values=array_map('stripslashes',$values);
	
	$values=array_map('htmlspecialchars',$values);
	
	$Template=new Template($values,'template/default.php');
	$body=$Template->output();
	
	$mail=new PHPMailer();
	
	$mail->CharSet='UTF-8';
	
	$mail->SetFrom($values['contact-form-mail'],$values['contact-form-name']); 
	$mail->AddReplyTo($values['contact-form-mail'],$values['contact-form-name']); 
	
	$mail->AddAddress(CONTACT_FORM_TO_EMAIL,CONTACT_FORM_TO_NAME);

	$smtp=CONTACT_FORM_SMTP_HOST;
	if(!empty($smtp))
	{
		$mail->IsSMTP();
		$mail->SMTPAuth=true; 
		$mail->Port=CONTACT_FORM_SMTP_PORT;
		$mail->Host=CONTACT_FORM_SMTP_HOST;
		$mail->Username=CONTACT_FORM_SMTP_USER;
		$mail->Password=CONTACT_FORM_SMTP_PASSWORD;
		/*$mail->SMTPSecure=CONTACT_FORM_SMTP_SECURE;*/
	}
	
	$mail->Subject=CONTACT_FORM_SUBJECT;
	$mail->MsgHTML($body);

	if(!$mail->Send())
	{
 		$response['error']=1;	
		$response['info'][]=array('fieldId'=>'contact-form-send','message'=>CONTACT_FORM_SEND_MSG_ERROR);
		createResponse($response);		
	}
	$response['error']=0;
	$response['info'][]=array('fieldId'=>'contact-form-send','message'=>CONTACT_FORM_SEND_MSG_OK);
	createResponse($response);

	/**************************************************************************/
	/**************************************************************************/
?>