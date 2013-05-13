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

var time_epoch = $.QueryString.usr;

$.ajax({ 
url: "data/dataout"+time_epoch+".json", 
cache: true,
	success: function(data){
		$("#coffee").find("coffeeName").text(data.coffee.coffee_name);
		$("#roaster").find("roastCompany").text(data.coffee.roast_company);
		$("#roaster").find("roastLocation").text(data.coffee.roast_location);
		$("#roast_image").attr("src", data.coffee.roast_image_url);
		$("#contact-form-coffee").attr("value", data.coffee.coffee_name);
		$("#contact-form-roast").attr("value", data.coffee.roast_company);
	},
	dataType: "json",
	cache: true
});

var id = response.info[1].fieldId;
alert(id);