import twitter
import config as cfg

def getTweetInfo(customer_name,blend_name,coffee_list):
	try:
		if blend_name in coffee_list:
			blend_name = blend_name + ' Single Origin'
		else:
			blend_name = blend_name + ' blend'
			
		tweet = '%s made a cup of the %s w/ the @BuildaBrew platform #coffee #tech. To learn more www.smartcoffeetech.com' % (customer_name,blend_name)
		return tweet
	except Exception, e:
		print e
	
		
def tweetIt(tweet_msg):
	try:
		my_auth = twitter.OAuth(cfg.TOKEN,cfg.TOKEN_KEY,cfg.CON_SEC,cfg.CON_SEC_KEY)
		twit = twitter.Twitter(auth=my_auth)
		twit.statuses.update(status=tweet_msg)
		print 'tweeted'
	except Exception, e:
		print e