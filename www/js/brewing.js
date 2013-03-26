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
	$.getJSON('dataout1.json', function(data){
		$("#coffee0").html("<b>" +Object.keys(data)[1]+": </b>" + data[Object.keys(data)[1]] + "%");
		$("#coffee1").html("<b>" +Object.keys(data)[5]+": </b>" + data[Object.keys(data)[5]] + "%");
		$("#coffee2").html("<b>" +Object.keys(data)[7]+": </b>" + data[Object.keys(data)[7]] + "%");
	});
	if (blend.substr(-5,5)=='Blend'){
		$("blendname").html("<strong> the </strong>" + blend);
	}
	else if (blend.substr(-8,8)=='Creation'){
		$("blendname").text(" your own " + blend);
	}
	else if (blend.substr(-6,6)=='Origin'){
		$("blendname").text(" "+ blend);
	}
});