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


function clicked(item) {
	var id;
    id = $(item).attr("id");
	$.cookie("roaster", id);
}

var time_epoch = $.QueryString.usr;

$.ajax({ 
url: "data/dataout"+time_epoch+".json", 
cache: true,
	success: function(data){
		$("#coffee").find("description").text(data.coffee.coffee_description);
		// $("#coffee").find("aromas").text(data.coffee.coffee_aromas);
		$("#roaster").find("coffeeName").text(data.coffee.coffee_name);
		$("#roaster").find("roastCompany").text(data.coffee.roast_company);
		$("#roaster").find("roastLocation").text(data.coffee.roast_location);
		$("#roast_image").attr("src", data.coffee.roast_image_url);
	},
	dataType: "json",
	cache: true
});
Shadowbox.init();

$(document).ready(function() {
	Shadowbox.init({ 
		language: "en", 
		players: ["html", "img", "iframe"] 
	}); 
	$("#whyThisCoffee").click(function(){
		Shadowbox.open({
		content:    'whythiscoffee.html',
		player:     "iframe",
		width:      1900,
		height:     1250
		})
	});
	$("#roasterInfo").click(function(){
		Shadowbox.open({
		content:    'roasterinfo.html',
		player:     "iframe",
		width:      1900,
		height:     1250
		})
	});
}); 