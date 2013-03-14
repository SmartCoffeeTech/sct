def letsCustomize():
	#look in db for a record that doesn't get
	customer_id,order_id,customer_name,blend_name = dbHandle.executeDbQuery(db_con,db_cur,query,'select')
	
	

def letsGrind(coffee_list,blend_filename,log_filename,ser,db_con,db_cur):
	
	#figure out what to do with that message
	if grinderCommManager(ser,msg_to_grinder).startswith('basePercentage'):
		grinder_pct_list,log_msg,grinder_status = parseMessageAndReturnInfo(message)
		
		try:
			
			if grinder_status.startswith('grind'):
				customer_id,order_id,customer_name,blend_name = dbHandle.executeDbQuery(db_con,db_cur,query,'select')
				coffee_dict = jaysohn.makeJson(coffee_list,grinder_pct_list,blend_name)
				jaysohn.postJsonToServer(blend_filename,coffee_dict)
				
				if sum(grinder_pct_list)==100:
					serialHandle.sendMesageToGrinder(ser,'complete')
					time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					customer_id,order_id,customer_name,blend_name = getFromDb(db_cur)
					dbHandle.executeDbQuery(db_cur,db_con,order_id,customer_id,grinder_pct_list,time)
					jaysohn.updateJson(blend_filename,'readyToBrew')
					tweet_msg = tweetHandle.getTweetInfo(customer_name,blend_name,coffee_list)
					tweetHandle.tweetIt(tweet_msg)
				
			elif grinder_status.startswith('comp'):
				jaysohn.updateJson(blend_filename,'complete')
				
			elif grinder_status.startswith('reset'):
				jaysohn.resetJsonFile(blend_filename)
				
		finally:
			logGrinderMessage(log_filename,log_msg)
			#db_cur.close()
			#db_con.close()