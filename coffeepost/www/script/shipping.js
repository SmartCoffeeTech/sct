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

$(document).ready(function(){ 
	
var time_epoch = $.QueryString.usr;

$("#contact-form-url").attr("value", time_epoch);


$.ajax({ 
url: "data/dataout"+time_epoch+".json", 
cache: false,
	success: function(data){
		$("#coffee").find("coffeeName").text(data.coffee_name);
		$("#roaster").find("roastCompany").text(data.roast_company);
		$("#roaster").find("roastLocation").text(data.roast_location);
		$("#roast_image").attr("src", data.roast_image_url);
		$("#contact-form-coffee").attr("value", data.coffee_name);
		$("#contact-form-roast").attr("value", data.roast_company);
	},
	dataType: "json",
	cache: false
});

});

var id = response.info[1].fieldId;
alert(id);