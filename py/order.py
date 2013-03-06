class Order(Blend):
	"""This class is used for creating the order and managing information"""
	
	def __init__(self,blend_name,time_created):
		self.name = name
		self.time_created = time_created
		
	def getOrderStartTime(self):
		"""Gets the precise time the order was placed."""
		return self.order_time_start
		
	#def sendSelectionToGrinders(self):
	#	serial.write(self.selection)
		
	def receiveDataFromGrinders(self):
		serial.read(arduino_serial_comm)
		
		
class Blend(object):
	"""This class is used for storing the Blend data """
	
	def __init__(self,name,description,location,farm):
		self.name = name
		self.description = description
		self.location = location
		self.farm = farm