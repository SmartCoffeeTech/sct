var cookieValue = $.cookie("roaster");

$(document).ready(function() {
if(cookieValue != 'roasterInfo'){
$.ajax({ 
url: "data/roasterInfo.json", 
cache: false,
	success: function(data){
		if(cookieValue == 'fourbarrel'){
		$("#coffee").find("roastCompany").text(data.fourbarrel.roast_company);
		$("#coffee").find("roastDescription").text(data.fourbarrel.roast_description);
		$("#roast_image").attr("src", data.fourbarrel.roast_image_url);
		$("#coffee").find("roastLocation").text(data.fourbarrel.roast_location);
		}
		else if(cookieValue == 'ritual'){
		$("#coffee").find("roastCompany").text(data.ritual.roast_company);
		$("#coffee").find("roastDescription").text(data.ritual.roast_description);
		$("#roast_image").attr("src", data.ritual.roast_image_url);
		$("#coffee").find("roastLocation").text(data.ritual.roast_location);
		}
		else if(cookieValue == 'bluebottle'){
		$("#coffee").find("roastCompany").text(data.bluebottle.roast_company);
		$("#coffee").find("roastDescription").text(data.bluebottle.roast_description);
		$("#roast_image").attr("src", data.bluebottle.roast_image_url);
		$("#coffee").find("roastLocation").text(data.bluebottle.roast_location);
		}
		else if(cookieValue == 'verve'){
		$("#coffee").find("roastCompany").text(data.verve.roast_company);
		$("#coffee").find("roastDescription").text(data.verve.roast_description);
		$("#roast_image").attr("src", data.verve.roast_image_url);
		$("#coffee").find("roastLocation").text(data.verve.roast_location);
		}
		else if(cookieValue == 'bicycle'){
		$("#coffee").find("roastCompany").text(data.bicycle.roast_company);
		$("#coffee").find("roastDescription").text(data.bicycle.roast_description);
		$("#roast_image").attr("src", data.bicycle.roast_image_url);
		$("#coffee").find("roastLocation").text(data.bicycle.roast_location);
		}
		else if(cookieValue == 'tico'){
		$("#coffee").find("roastCompany").text(data.tico.roast_company);
		$("#coffee").find("roastDescription").text(data.tico.roast_description);
		$("#roast_image").attr("src", data.tico.roast_image_url);
		$("#coffee").find("roastLocation").text(data.tico.roast_location);
		}
	},
	dataType: "json",
	cache: false
});
}
else if(cookieValue == 'roasterInfo'){
$.ajax({ 
url: "data/dataout.json", 
cache: false,
	success: function(data){
		$("#coffee").find("roastCompany").text(data.coffee.roast_company);
		$("#coffee").find("roastDescription").text(data.coffee.roast_description);
		$("#coffee").find("roastLocation").text(data.coffee.roast_location);
		$("#roast_image").attr("src", data.coffee.roast_image_url);
	},
	dataType: "json",
	cache: false
});
}
});