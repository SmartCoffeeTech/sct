import twitter
import config as cfg

def getTweetInfo(customer_name,blend_name,coffee_list):
	if blend_name in coffee_list:
		blend_name = blend_name + ' Single Origin'
	else:
		blend_name = blend_name + ' blend'
		
	tweet = '%s made a cup of the %s w/ the @BuildaBrew platform #coffee #tech. To learn more http://bit.ly/14X7wxa' % (customer_name,blend_name)
	print tweet
	return tweet
	

def tweetIt(tweet_msg):
	my_auth = twitter.OAuth(cfg.TOKEN,cfg.TOKEN_KEY,cfg.CON_SEC,cfg.CON_SEC_KEY)
	twit = twitter.Twitter(auth=my_auth)
	twit.statuses.update(status=tweet_msg)
	print 'tweeted'

customer_name = 'Kevin'
blend_name = 'Ethiopian'
coffee_list = ['Ethiopian','Colombian','Indonesian']

tweet_msg = getTweetInfo(customer_name,blend_name,coffee_list)
tweetIt(tweet_msg)