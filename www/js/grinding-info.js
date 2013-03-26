$(document).ready(function() {
	setInterval(function(){
		$.ajax({ 
		url: "../data/dataout2.json", 
			success: function(data){
				if (data.button=='pressed'){
					$("#centerArea").css('opacity', 0.3);
					$("#rightArea").css('opacity', 0.3);
					$('#slider').data('nivoslider').stop(); 
				}

				var coffeeAcidity = (data.customerBody-6)*(25);
				var customerAcidity = (data.customerAcidity-6)*(25);
				var coffeeBody = (data.customerBody-6)*(25);
				var customerBody = (data.customerBody-6)*(25);
				var progressBarLevel = (data.customerPercentages.grinder0Percentage)+(data.customerPercentages.grinder1Percentage)+(data.customerPercentages.grinder2Percentage);

				$("#progressBar").width(progressBarLevel+'%');

				$("#coffeeAcidity").height(coffeeAcidity+'%');
				$("#customerAcidity").height(customerAcidity+'%');

				$("#coffeeBody").height(coffeeBody+'%');
				$("#customerBody").height(customerBody+'%');

				$("#coffeeDetails").find("country").text(data.coffee.country_of_origin);
				$("#coffeeDetails").find("region").text(data.coffee.region);

				$("#farm_image1").attr("src", data.coffee.farm_image1_url);
				$("#farm_image2").attr("src", data.coffee.farm_image2_url);
				$("#farm_image3").attr("src", data.coffee.farm_image3_url);

				$("#farmDetails").find("farm").text(data.coffee.farm);
				$("#farmDetails").find("altitude").text(data.coffee.altitude);

				$("#roast_company").find("roaster").text(data.coffee.roast_company);
				$("#roaster_image").attr("src", data.coffee.roaster_image_url);

				$("#aromas").find("aroma1").text(data.coffee.aroma1);
				$("#aromas").find("aroma2").text(data.coffee.aroma2);
				$("#aromas").find("aroma3").text(data.coffee.aroma3);
			},
			dataType: "json",
			cache: false
		});
},10); 

	$(window).load(function() {
	    $('#slider').nivoSlider({
	        effect: 'none', // Specify sets like: 'fold,fade,sliceDown'
	        animSpeed: 500, // Slide transition speed
	        pauseTime: 5000, // How long each slide will show
	        startSlide: 0, // Set starting Slide (0 index)
	        directionNav: false, // Next & Prev navigation
	        controlNav: false, // 1,2,3... navigation
	        controlNavThumbs: false, // Use thumbnails for Control Nav
	        pauseOnHover: false, // Stop animation while hovering
	        manualAdvance: false, // Force manual transitions
	        prevText: 'Prev', // Prev directionNav text
	        nextText: 'Next', // Next directionNav text
	        randomStart: false, // Start on a random slide
	    });
	});
});