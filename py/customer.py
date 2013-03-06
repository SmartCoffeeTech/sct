#the customer class for placing orders on build-a-brew
#person becomes A customer when they place an order
#an order can either be customer or a blend
#a customer order 0 gives the customer control - show percentage remaining
#when the max is reached - ready to brew - the order is complete
#a customer order 1-9 gives the bustomer a blend - show blend info
#when the customer goes to each grinder they have a limited time

class Customer:
	"""This class is used for creating the Customer and manging customer information"""
	
	def __init__(self,name,time_created):
		self.name = name
		self.time_created = time_created
		
	def getOrderStartTime(self):
		"""Gets the precise time the order was placed."""
		return self.order_time_start
		
	#def sendSelectionToGrinders(self):
	#	serial.write(self.selection)
		
	def receiveDataFromGrinders(self):
		serial.read(arduino_serial_comm)
	
	

# print Customer.__doc__
# print Customer.getOrderTime.__doc__
		
	