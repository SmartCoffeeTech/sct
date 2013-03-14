def testIt(bacon,newbacon):
	if bacon=='ready':
		try:
			if newbacon=='super_ready':
				print 'cooking...'
			else:
				raise Exception("invalid message")
		except Exception, e:
			print 'You raised an exception with the grinder...'
			exceptionHandler()
			testIt('ready','super_ready')

			
def exceptionHandler():
	print 'we called this exception handler func!'

testIt('ready','super_ready23')
testIt('ready','super_ready')
