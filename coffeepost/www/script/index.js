
Shadowbox.init();

function clicked(item) {
	var id;
    id = $(item).attr("id");
	$.cookie("roaster", id);
}

$(document).ready(function() {
	Shadowbox.init({ 
		language: "en", 
		players: ["html", "img", "iframe"] 
	}); 

	$(".roasterInfo").click(function(){
		Shadowbox.open({
		content:    'roasterInfo.html',
		player:     "iframe",
		width:      1900,
		height:     1250
		})
	});
}); 