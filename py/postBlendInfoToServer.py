def postBlendInfoToServer(filename,grinder_pct_list,blend_name='Blend',coffee_list=[],tweet=''):
	
	if grinder_pct_list!='NULL':
		
		if len(coffee_list)==0:
			coffeeDict = {
		    "blendRecipe": blend_name,
		    "grinderPercentage0": grinder_pct_list[0],
			"grinderPercentage1": grinder_pct_list[1],
			"grinderPercentage2": grinder_pct_list[2],
			"readyToBrew":'False'
			}
		
		elif len(coffee_list)>0:
			
			coffeeDict = {
		    "blendRecipe": blend_name,
			coffee_list[0]: grinder_pct_list[0],
			coffee_list[1]: grinder_pct_list[1],
			coffee_list[2]: grinder_pct_list[2],
			"readyToBrew":'False'
			}
		
	elif grinder_pct_list=='NULL':
		
		if tweet=='':
			coffeeDict = {
			"readyToBrew":'True'
			}
	
		elif tweet=='yes':
			
			coffeeDict = {
			"tweeted":'True'
			}
	
	print coffeeDict
	file = open(filename,'w+')
	file.write(json.dumps(coffeeDict))
	file.close()

postBlendInfoToServer(filename,grinder_pct_list,blend_name='Blend',coffee_list=[],tweet=''):
postBlendInfoToServer(blend_filename,grinder_pct_list,blend_name)
postBlendInfoToServer(coffee_blend_filename,grinder_pct_list,coffee_list)
postBlendInfoToServer(blend_filename,grinder_pct_list)
postBlendInfoToServer(blend_filename,grinder_pct_list,'yes')