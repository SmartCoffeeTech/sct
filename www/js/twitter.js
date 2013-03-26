$(document).ready(function() {
	setInterval(function(){
	    $.ajax({ 
		url: "../data/dataout2.json",
			success: function(data){
				if(data.status=='complete'){
					var url = "index1.html";
					setTimeout(function(){$(location).attr('href',url);}, 10);
				}
		   },
		dataType: "json",
		cache: false
		});
	},110);
});