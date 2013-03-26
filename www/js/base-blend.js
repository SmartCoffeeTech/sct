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
	$("h1").text("Thanks "+$.QueryString.name+", Now Pick an Option Below!");

	$("#show_div_base").mouseover(function(){ $("#detail").css('visibility','visible');});
	$("#show_div_base").mouseover(function(){ $("#intro").css('visibility','hidden');});    
	$("#show_div_base").mouseover(function(){ $("#detail").find("name").text("Base Blend");});
	$("#show_div_base").mouseover(function(){ $("#detail").find("coffee1").text("?%");});
	$("#show_div_base").mouseover(function(){ $("#detail").find("coffee2").text("?%");});
	$("#show_div_base").mouseover(function(){ $("#detail").find("coffee3").text("?%");});
	$("#show_div_base").mouseout(function() { $("#detail").css('visibility','hidden');});
	$("#show_div_base").mouseout(function() { $("#intro").css('visibility','visible');}); 

	$("#show_div_full").mouseover(function(){ $("#detail").css('visibility','visible');});
	$("#show_div_full").mouseover(function(){ $("#intro").css('visibility','hidden');});
	$("#show_div_full").mouseover(function(){ $("#detail").find("name").text("Suggested Blend");});    
	$("#show_div_full").mouseover(function(){ $("#detail").find("coffee1").text("?%");});
	$("#show_div_full").mouseover(function(){ $("#detail").find("coffee2").text("?%");});
	$("#show_div_full").mouseover(function(){ $("#detail").find("coffee3").text("?%");});
	$("#show_div_full").mouseout(function() { $("#detail").css('visibility','hidden');});
	$("#show_div_full").mouseout(function() { $("#intro").css('visibility','visible');}); 
});
