	
    /*****************************************************************/
    /*****************************************************************/
	
	function submitNewsletterForm()
	{
		blockForm('newsletter-form','block');
		$.post('plugin/newsletter-form/newsletter-form.php',$('#newsletter-form').serialize(),submitNewsletterFormResponse,'json');
	}
	
	/*****************************************************************/
	
	function submitNewsletterFormResponse(response)
	{
        blockForm('newsletter-form','unblock');
        $('#newsletter-form-mail,#newsletter-form-send').qtip('destroy');

        var tPosition=
        {
            'newsletter-form-send'		: {'my':'right center','at':'left center'},
            'newsletter-form-mail'		: {'my':'bottom center','at':'top center'}
        };

        if(typeof(response.info)!='undefined')
        {	
            if(response.info.length)
            {	
                for(var key in response.info)
                {
                    var id=response.info[key].fieldId;
                    $('#'+response.info[key].fieldId).qtip(
                    {
                            style:      { classes:(response.error==1 ? 'ui-tooltip-error' : 'ui-tooltip-success')},
                            content: 	{ text:response.info[key].message },
                            position: 	{ my:tPosition[id]['my'],at:tPosition[id]['at'] }
                    }).qtip('show');				
                }
            }
        }
	}
	
	/*****************************************************************/
	/*****************************************************************/	