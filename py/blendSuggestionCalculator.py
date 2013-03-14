#do some shit
#each blend has a profile
#compare the customer profile selection to the blend
#compute the available blends

#coffee_attributes json gets entered manually
blend = '{"name":"Golden Gate",        "body":9.0,"acidity":5.5,"fruity":3,"earthy":3,"chocolatey":5,"winey":6,"nutty":5,"herby":3,"smokey":3,"spicy":3,"floral":3}'
blend1 = '{"name":"Stanford Cardinal", "body":8.3,"acidity":6.5,"fruity":3,"earthy":3,"chocolatey":5,"winey":6,"nutty":5,"herby":3,"smokey":3,"spicy":5,"floral":6}'
blend2 ='{"name":"Shreveport John",    "body":9.1,"acidity":7.5,"fruity":2,"earthy":4,"chocolatey":3,"winey":4,"nutty":6,"herby":4,"smokey":6,"spicy":4,"floral":7}'
blend3 ='{"name":"Johan Gutenburg",    "body":6.9,"acidity":8.5,"fruity":1,"earthy":5,"chocolatey":7,"winey":8,"nutty":5,"herby":5,"smokey":4,"spicy":3,"floral":2}'
blend = json.loads(blend)
blend1 = json.loads(blend1)
blend2 = json.loads(blend2)
blend3 = json.loads(blend3)

coffee1 = '{"name":"Ethiopian",  "body":2.3,"acidity":4.5,"fruity":6,"earthy":8,"chocolatey":5,"winey":4,"nutty":3,"herby":2,"smokey":3,"spicy":7,"floral":5}'
coffee2 ='{"name":"Colombian",   "body":9.1,"acidity":2.5,"fruity":4,"earthy":4,"chocolatey":3,"winey":2,"nutty":7,"herby":6,"smokey":6,"spicy":4,"floral":9}'
coffee3 ='{"name":"Costa Rican", "body":4.9,"acidity":5.5,"fruity":2,"earthy":3,"chocolatey":7,"winey":10,"nutty":5,"herby":8,"smokey":4,"spicy":2,"floral":2}'


cust1 = '{"body" : 5.0, "acidity":5.0, "fruity":1, "earthy":0, "chocolatey":0,"winey":1,"nutty":0,"herby":1,"smokey":0,"spicy":0,"floral":0}'
cust2 = '{"body" : 5.0, "acidity":5.0, "fruity":0, "earthy":1, "chocolatey":1,"winey":0,"nutty":0,"herby":0,"smokey":0,"spicy":1,"floral":0}'
cust3 = '{"body" : 1.0, "acidity":1.0, "fruity":0, "earthy":0, "chocolatey":0,"winey":0,"nutty":1,"herby":0,"smokey":1,"spicy":0,"floral":1}'
cust4 = '{"body" : 6.9, "acidity":5.5, "fruity":0, "earthy":0, "chocolatey":0,"winey":0,"nutty":1,"herby":0,"smokey":1,"spicy":0,"floral":1}'

cust1 = json.loads(cust1)
cust2 = json.loads(cust2)
cust3 = json.loads(cust3)
cust4 = json.loads(cust4)

for x_values, y_values in zip(blend.iterkeys(), cust1.iterkeys()):
        if x_values == y_values:
            print 'Ok', x_values, y_values
        else:
            print 'Not', x_values, y_values

def computeCoffeeRating(blend_dict,cust):
	distance_from_attributes = 0
	distance_from_blend = 1
	
	blend = blend_dict.copy()
	del blend['name']
	
	for x_values, y_values in zip(blend.iteritems(), cust.iteritems()):
		if x_values[0] == y_values[0]:
			if x_values[0] in ['body','acidity']:
				#print x_values[0], y_values[0]
				#print 1-((x_values[1]-y_values[1])/float((x_values[1])))
				distance_from_blend *= 1 - (abs((x_values[1]-y_values[1]))/(float(x_values[1])))
			else:
				#print x_values[0], y_values[0]
				#print x_values[1]*y_values[1]
				distance_from_attributes += x_values[1]*y_values[1]
	
	f_max,w_max,h_max = 3,8,5
	distance_from_attributes = distance_from_attributes/float((f_max+w_max+h_max))
	#add spacing here
	#print distance_from_blend
	#print distance_from_attributes
	print 'final rating:', blend_dict['name'], distance_from_blend*distance_from_attributes
	blend_proximity = distance_from_blend*distance_from_attributes
	return blend_dict['name'],blend_proximity

def computeCoffeeBlend(blends,cust):
	best_rating = 0
	for each_blend in blends:
		blend_name,blend_proximity = computeCoffeeRating(each_blend,cust)
		if blend_proximity > best_rating: 
			best_rating = blend_proximity
			best_blend_name = blend_name
	print best_blend_name, ':', best_rating

computeCoffeeBlend([blend,blend1,blend2,blend3],cust4)