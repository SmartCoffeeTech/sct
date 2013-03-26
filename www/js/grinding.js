Shadowbox.init();

(function($) {
    $.QueryString = (function(a) {
        if (a == "") return {};
        var b = {};
        for (var i = 0; i < a.length; ++i)
        {
            var p=a[i].split('=');
            if (p.length != 2) continue;
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }
        return b;
    })(window.location.search.substr(1).split('&'))
})(jQuery);

$(document).ready(function() {

	$("h1").text("Grind Your "+$.QueryString.blend+"!");          
	              
	var coffeegage0 = new JustGage({
		id: "gage0",
		value: 50,
		min: 0,
		max: 100,
		gaugeWidthScale : 1.3,
		gaugeColor :  "#cccccc",
		levelColors : ["#62c462","#62c462","#62c462"],
		showMinMax : false,
		title: " "
	});    
	  
	var coffeegage1 = new JustGage({
		id: "gage1",
		value: 10,
		min: 0,
		max: 100,
		gaugeWidthScale : 1.3,
		gaugeColor :  "#cccccc",
		levelColors : ["#faa732","#faa732","#faa732"],
		showMinMax : false,
		title: " "
	}); 
  			  
	var coffeegage2 = new JustGage({
		id: "gage2",
		value: 10,
		min: 0,
		max: 100,
		gaugeWidthScale : 1.3,
		gaugeColor :  "#cccccc",
		levelColors : ["#ee5f5b","#ee5f5b","#ee5f5b"],
		showMinMax : false,
		title: " "
	}); 

	Shadowbox.init({ 
		language: "en", 
		players: ["html", "img", "iframe"] 
	}); 

	setInterval(function(){
	    $.ajax({ 
		url: "../data/dataout2.json", 
			success: function(data){
				if (data.canister=='true'){
					Shadowbox.open({
					content:    'grinder-info.html',
					player:     "iframe",
					height:     510,
                    width:      930,
                    displayNav: false
				});
				}

				else if (data.canister=='false'){
						Shadowbox.close();
				}

				var totalGround = (data.customerPercentages.grinder0Percentage)+(data.customerPercentages.grinder1Percentage)+(data.customerPercentages.grinder2Percentage);	
				var basePercentage = (data.blendPercentages.grinder0Percentage)+(data.blendPercentages.grinder1Percentage)+(data.blendPercentages.grinder2Percentage);	
				
				if (data.status=='grinding' || data.status=='readyToBrew'){
					if (totalGround==0 && data.state=='base'){
						if (data.blendPercentages.grinder0Percentage!=0){
							$("#indicator0check").show();
							$("#indicator0cross").hide();
						}
							else{
								$("#indicator0cross").show();
								$("#indicator0check").hide();
							}
						if (data.blendPercentages.grinder1Percentage!=0){
							$("#indicator1check").show();
							$("#indicator1cross").hide();
						}
							else{
								$("#indicator1cross").show();
								$("#indicator1check").hide();
							}
						if (data.blendPercentages.grinder2Percentage!=0){
							$("#indicator2check").show();
							$("#indicator2cross").hide();
						}
							else{
								$("#indicator2cross").show();
								$("#indicator2check").hide();
							}
					}

					else if (totalGround!=0 && data.state=='base'){
						if (data.customerPercentages.grinder0Percentage!=0){
							$("#indicator0star").show();
							$("#indicator0check").hide();
							$("#indicator0cross").hide();
							$("#coffeebar0").width(data.overall.customerPercentages.grinder0Percentage+'%');
						}
						if (data.customerPercentages.grinder1Percentage!=0){
							$("#indicator1star").show();
							$("#indicator1check").hide();
							$("#indicator1cross").hide();
							$("#coffeebar1").width(data.customerPercentages.grinder1Percentage+'%');
						}
						if (data.customerPercentages.grinder2Percentage!=0){
							$("#indicator2star").show();
							$("#indicator2check").hide();
							$("#indicator2cross").hide();
							$("#coffeebar2").width(data.customerPercentages.grinder2Percentage+'%');
						}
						if (data.status=='readyToBrew'){
						var url = "brewing.html";
						setTimeout(function(){$(location).attr('href',url);}, 1900);
						}	
					}
				}

				if (data.status=='grinding' || data.status=='readyToBrew'){
					if (totalGround==basePercentage && data.state=='custom'){
						$("#coffeebar0").width(data.customerPercentages.grinder0Percentage+'%');
						$("#coffeebar1").width(data.customerPercentages.grinder1Percentage+'%');
						$("#coffeebar2").width(data.customerPercentages.grinder2Percentage+'%');
						coffeegage0.refresh(data.customerPercentages.grinder0Percentage);  
			  			coffeegage1.refresh(data.customerPercentages.grinder1Percentage);
			  			coffeegage2.refresh(data.customerPercentages.grinder2Percentage);

						$("#gage0").show();
						$("#indicator0star").hide();
						$("#indicator0check").hide();
						$("#indicator0cross").hide();
						$("#gage1").show();
						$("#indicator1star").hide();
						$("#indicator1check").hide();
						$("#indicator1cross").hide();
						$("#gage2").show();
						$("#indicator2star").hide();
						$("#indicator2check").hide();
						$("#indicator2cross").hide();
					}

					if (totalGround!=basePercentage && data.state=='custom'){
						$("#coffeebar0").width(data.customerPercentages.grinder0Percentage+'%');
						$("#coffeebar1").width(data.customerPercentages.grinder1Percentage+'%');
						$("#coffeebar2").width(data.customerPercentages.grinder2Percentage+'%');
						coffeegage0.refresh(data.customerPercentages.grinder0Percentage);  
			  			coffeegage1.refresh(data.customerPercentages.grinder1Percentage);
			  			coffeegage2.refresh(data.customerPercentages.grinder2Percentage);
					}			
					if (data.status=='readyToBrew'){
						var url = "brewing.html";
						setTimeout(function(){$(location).attr('href',url);}, 1900);
					}	
				}
	
		   },
		dataType: "json",
		cache: false
		});
	},100); 		
});
