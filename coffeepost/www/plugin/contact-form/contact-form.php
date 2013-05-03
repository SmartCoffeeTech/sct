<?php

	/**************************************************************************/
	/**************************************************************************/
	
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
		'contact-form-number'					=> $_POST['contact-form-number'],
		'contact-form-roast'					=> $_POST['contact-form-roast'],		
		'contact-form-coffee'					=> $_POST['contact-form-coffee'],
		'contact-form-message'					=> $_POST['contact-form-message']
	);
	
	/**************************************************************************/
	
	if(isEmpty($values['contact-form-name']))
	{
		$response['error']=1;
		$response['info'][]=array('fieldId'=>'contact-form-name','message'=>CONTACT_FORM_MSG_INVALID_DATA_NAME);
	}

	if(isEmpty($values['contact-form-number']))
	{
		$response['error']=1;
		$response['info'][]=array('fieldId'=>'contact-form-number','message'=>CONTACT_FORM_MSG_INVALID_DATA_NUMBER);
	}
	
	if(!validateEmail($values['contact-form-mail']))
	{
 		$response['error']=1;	
		$response['info'][]=array('fieldId'=>'contact-form-mail','message'=>CONTACT_FORM_MSG_INVALID_DATA_MAIL);
	}
	
	if(isEmpty($values['contact-form-message']))
	{
		$response['error']=1;
		$response['info'][]=array('fieldId'=>'contact-form-message','message'=>CONTACT_FORM_MSG_INVALID_DATA_MESSAGE);
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