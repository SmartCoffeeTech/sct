def ab(ab):
	try:
		if ab=='ok':
			print 'we are good'
		else:
			raise Exception('fucked')
	except Exception, e:
		print e


if __name__=='__main__':
	while True:
		try:
			ab('chicken')
			ab('ok')
		except Exception, e:
			print e
