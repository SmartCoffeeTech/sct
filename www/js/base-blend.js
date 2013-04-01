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

	$.getJSON("../data/dataout2.json",
		function(data){
            var aroma1 = data.blendAromas.aroma1;
            var aroma2 = data.blendAromas.aroma2;                                                            
            var aroma3 = data.blendAromas.aroma3;

            $("#detail").find("aroma1").text(aroma1);
            $("#detail").find("aroma2").text(aroma2);
            $("#detail").find("aroma3").text(aroma3);

            $("#detail").find("name2").css('opacity', .5);
            $("#detail").find("name3").css('opacity', .5);      

            if (data.blendAromas.name=='Stanford Cardinal'){
            $("#detail").find("name1").text("Stanford Cardinal");
            }

            if (data.blendAromas.name=='Fog City'){
            $("#detail").find("name1").text("Fog City");                                                      
            }                                                             

            if (data.blendAromas.name=='Golden Gate'){
            $("#detail").find("name1").text("Golden Gate");

            }             
            });
});