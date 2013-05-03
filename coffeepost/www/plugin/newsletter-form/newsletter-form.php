<?php

	/**************************************************************************/
	/**************************************************************************/

	require_once('config.php');
	require_once('../../include/functions.php');
	
	/**************************************************************************/
	
	$response=array('error'=>0,'info'=>null);

	$values=array
	(
		'newsletter-form-mail'		=> $_POST['newsletter-form-mail']
	);
	
	if(isGPC()) $values=array_map('stripslashes',$values);
	
	/**************************************************************************/
	
	if(!validateEmail($values['newsletter-form-mail']))
	{
 		$response['error']=1;	
		$response['info'][]=array('fieldId'=>'newsletter-form-mail','message'=>NEWSLETTER_FORM_MSG_INVALID_DATA_MAIL);
		createResponse($response);
	}
	
	/**************************************************************************/
	
	if(($handle=fopen(NEWSLETTER_FORM_DATA_FILE_PATH,'a+'))===false)
	{
 		$response['error']=1;	
		$response['info'][]=array('fieldId'=>'newsletter-form-send','message'=>NEWSLETTER_FORM_MSG_FILE_ERROR);
		createResponse($response);		
	}
	
	/**************************************************************************/
	
	if(($emails=@split("\n",fread($handle,filesize(NEWSLETTER_FORM_DATA_FILE_PATH))))===false)
	{
 		$response['error']=1;	
		$response['info'][]=array('fieldId'=>'newsletter-form-send','message'=>NEWSLETTER_FORM_MSG_FILE_ERROR);
		createResponse($response);		
	}
	
	/**************************************************************************/
	
	$values['newsletter-form-mail']=strtolower($values['newsletter-form-mail']);
	if(in_array($values['newsletter-form-mail'],$emails))
	{
  		$response['error']=1;		
		$response['info'][]=array('fieldId'=>'newsletter-form-mail','message'=>NEWSLETTER_FORM_MSG_MAIL_EXIST);
		createResponse($response);	
	}
	
	/**************************************************************************/
	
	if(fwrite($handle,$values['newsletter-form-mail']."\n")===false)
	{
  		$response['error']=1;		
		$response['info'][]=array('fieldId'=>'newsletter-form-send','message'=>NEWSLETTER_FORM_MSG_FILE_ERROR);
		createResponse($response);		
	}
	
	/**************************************************************************/
	
	$response['error']=0;	
	$response['info'][]=array('fieldId'=>'newsletter-form-send','message'=>NEWSLETTER_FORM_SEND_MSG_OK);
	createResponse($response);		
	
	/**************************************************************************/	
	/**************************************************************************/
	
?>