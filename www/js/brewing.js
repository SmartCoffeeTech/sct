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
	var blend = $.QueryString.blend;
	$.getJSON('../data/dataout2.json', function(data){
		// $("#coffee0").html("<b>" +Object.keys(data)[1]+": </b>" + data[Object.keys(data)[1]] + "%");
		// $("#coffee1").html("<b>" +Object.keys(data)[5]+": </b>" + data[Object.keys(data)[5]] + "%");
		// $("#coffee2").html("<b>" +Object.keys(data)[7]+": </b>" + data[Object.keys(data)[7]] + "%");
		$("#coffee0").html("<b>Ethiopian: </b>" + data.customerPercentages.grinder0Percentage + "%");
		$("#coffee1").html("<b>Bolivian: </b>" + data.customerPercentages.grinder1Percentage + "%");
		$("#coffee2").html("<b>Indonesian: </b>" + data.customerPercentages.grinder2Percentage + "%");
		$("#aroma1").find("aroma1").text(data.blendAromas.aroma1);
	    $("#aroma2").find("aroma2").text(data.blendAromas.aroma2);
	    $("#aroma3").find("aroma3").text(data.blendAromas.aroma3);
	});
});