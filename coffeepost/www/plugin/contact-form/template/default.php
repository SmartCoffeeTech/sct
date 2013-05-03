<html>

	<head>

	</head>

	<body>

		<div><b>Name</b>: <?php echo $this->data['contact-form-name']; ?></div>
		<div><b>E-mail</b>: <?php echo $this->data['contact-form-mail']; ?></div>
		<div><b>Phone Number</b>: <?php echo $this->data['contact-form-number']; ?></div>
		<div><b>Roaster</b>: <?php echo $this->data['contact-form-roast']; ?></div>		
		<div><b>Coffee</b>: <?php echo $this->data['contact-form-coffee']; ?></div>
		<div><b>Address</b>: <?php echo nl2br($this->data['contact-form-message']); ?></div>

	</body>

</html>
