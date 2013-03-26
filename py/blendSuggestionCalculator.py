#do some shit
#each blend has a profile
#compare the customer profile selection to the blend
#compute the available blends
import json
#coffee_attributes json gets entered manually
import collections

def initData(selection):
	
	blend = '{"name":"Golden Gate",        "body":9.0,"acidity":5.5,"fruity":3,"earthy":3,"chocolatey":5,"winey":6,"nutty":5,"herby":3,"smokey":3,"spicy":3,"floral":3}'
	blend1 = '{"name":"Stanford Cardinal", "body":8.3,"acidity":6.5,"fruity":3,"earthy":3,"chocolatey":5,"winey":6,"nutty":5,"herby":3,"smokey":3,"spicy":5,"floral":6}'
	blend2 ='{"name":"Fog City",    "body":9.1,"acidity":7.5,"fruity":2,"earthy":4,"chocolatey":3,"winey":4,"nutty":6,"herby":4,"smokey":6,"spicy":4,"floral":7}'
	# blend3 ='{"name":"Johan Gutenburg",    "body":6.9,"acidity":8.5,"fruity":1,"earthy":5,"chocolatey":7,"winey":8,"nutty":5,"herby":5,"smokey":4,"spicy":3,"floral":2}'
	blend = json.loads(blend)
	blend1 = json.loads(blend1)
	blend2 = json.loads(blend2)
	# blend3 = json.loads(blend3)
	
	coffee1 = '{"name":"Ethiopian",  "body":2.3,"acidity":4.5,"fruity":6,"earthy":8,"chocolatey":5,"winey":4,"nutty":3,"herby":2,"smokey":3,"spicy":7,"floral":5}'
	coffee2 ='{"name":"Colombian",   "body":9.1,"acidity":2.5,"fruity":4,"earthy":4,"chocolatey":3,"winey":2,"nutty":7,"herby":6,"smokey":6,"spicy":4,"floral":9}'
	coffee3 ='{"name":"Costa Rican", "body":4.9,"acidity":5.5,"fruity":2,"earthy":3,"chocolatey":7,"winey":10,"nutty":5,"herby":8,"smokey":4,"spicy":2,"floral":2}'
	json.loads(coffee1)
	json.loads(coffee2)
	json.loads(coffee3)
	
	cust1 = '{"body" : 5.0, "acidity":5.0, "fruity":1, "earthy":0, "chocolatey":0,"winey":1,"nutty":0,"herby":1,"smokey":0,"spicy":0,"floral":0}'
	cust2 = '{"body" : 5.0, "acidity":5.0, "fruity":0, "earthy":1, "chocolatey":1,"winey":0,"nutty":0,"herby":0,"smokey":0,"spicy":1,"floral":0}'
	cust3 = '{"body" : 1.0, "acidity":1.0, "fruity":0, "earthy":0, "chocolatey":0,"winey":0,"nutty":1,"herby":0,"smokey":1,"spicy":0,"floral":1}'
	cust4 = '{"body" : 6.9, "acidity":5.5, "fruity":0, "earthy":0, "chocolatey":0,"winey":0,"nutty":1,"herby":0,"smokey":1,"spicy":0,"floral":1}'
	cust1 = json.loads(cust1)
	cust2 = json.loads(cust2)
	cust3 = json.loads(cust3)
	cust4 = json.loads(cust4)
		
	if selection=='coffee':	
		coffee_list = []
		coffee_list = [coffee1,coffee2,coffee3]
		return coffee_list
	elif selection=='blend':	
		blend_list = []
		blend_list = [blend,blend1,blend2,blend3]
		return blend_list
	elif selection=='customer':	
		customer_list = []
		customer_list = [cust1,cust2,cust3,cust4]
		return customer_list

def justAFunc():
	for x_values, y_values,z_values in zip(blend.iterkeys(), cust1.iterkeys(), blend2.iterkeys()):
		if x_values == y_values:
			print 'Ok', blend[x_values], y_values,z_values
			print 'values', x_values[0], y_values[0]
		else:
			print 'Not', x_values, y_values
		
def computeTop3Aromas(blend_dict):
	blend_dict_copy = blend_dict.copy()
	aroma_dict = {}
	
	for each_value in ['name','body','acidity']:
		del blend_dict_copy[each_value]
		
	aromas = sorted(blend_dict_copy, key=blend_dict_copy.get, reverse=True)[:3]
	
	aroma_dict['name']=blend_dict['name']
	
	i=1
	for each in aromas:
		aroma_dict['aroma'+str(i)]=each
		i+=1
		
	return aroma_dict
	

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
	
	#update this actual values
	f_max,w_max,h_max = 6,10,8
	distance_from_attributes = distance_from_attributes/float((f_max+w_max+h_max))
	#add spacing here
	#print distance_from_blend
	#print distance_from_attributes
	print 'final rating:', blend_dict['name'], distance_from_blend*distance_from_attributes
	blend_proximity = distance_from_blend*distance_from_attributes
	return blend_dict['name'],blend_proximity

def computeCoffeeBlendSuggestion(blends,cust):
	best_rating = 0
	for each_blend in blends:
		blend_name,blend_proximity = computeCoffeeRating(each_blend,cust)
		if blend_proximity > best_rating: 
			best_rating = blend_proximity
			best_blend_name = blend_name
	# print best_blend_name, ':', best_rating
	return best_blend_name
	
#for this to work:
# 
def computeCoffeeChange(cp_list=[],bp_list=[],blend={},blend_percentage=0):
	coffee1 = {"name":"Ethiopian",  "body":2.3,"acidity":4.5,"fruity":6,"earthy":8,"chocolatey":5,"winey":4,"nutty":3,"herby":2,"smokey":3,"spicy":7,"floral":5}
	coffee2 = {"name":"Colombian",   "body":9.1,"acidity":2.5,"fruity":4,"earthy":4,"chocolatey":3,"winey":2,"nutty":7,"herby":6,"smokey":6,"spicy":4,"floral":9}
	coffee3 = {"name":"Costa Rican", "body":4.9,"acidity":5.5,"fruity":2,"earthy":3,"chocolatey":7,"winey":10,"nutty":5,"herby":8,"smokey":4,"spicy":2,"floral":2}
	
	
	if len(cp_list)==0:
		#percentage of coffee in the cup
		cp1 = 20
		cp2 = 40
		cp3 = 10
		#percentage of coffee as dictated by the blend
		bp1 = 20
		bp2 = 40
		bp3 = 10
		#acidity of each coffee
		a1 = 8.3
		a2 = 6.4
		a3 = 8.1
		#body of each coffee
		b1 = 8.3
		b2 = 6.4
		b3 = 8.1
		# acidity of the blend
		Ab = 6.0
		#Body of the blend
		Bb = 5.3
		#Blendpercentage (100-customization <- from db -> Orders.customization_pct)
		Bp = 70
	else:
		cp1,cp2,cp3 = cp_list
		bp1,bp2,bp3 = bp_list
		a1,a2,a3 = coffee1['acidity'],coffee2['acidity'],coffee3['acidity']
		b1,b2,b3 = coffee1['body'],coffee2['body'],coffee3['body']
		Ab = blend['acidity']
		Bb = blend['body']
		Bp = blend_percentage #base_pct
	
	#Total Percentage sum (grinder values)
	Tp = cp1+cp2+cp3
	#Acidity of the cup
	Ac = (((cp1-bp1)*a1) + ((cp2-bp2)*a2) + ((cp3-bp3)*a3) + (Bp*Ab))/Tp
	#Body of the cup
	Bc = (((cp1-bp1)*b1) + ((cp2-bp2)*b2) + ((cp3-bp3)*b3) + (Bp*Bb))/Tp
	print Ac, Bc
	return Ac,Bc
	
def computeBlendPct(grinder_pct_list=0,custom_pct=0):
	grinder_pct_list = [20,40,40]
	if custom_pct!=0:
		blend_pct = float(sum(grinder_pct_list)-custom_pct)/100
		grinder_pct_list[0] = int(blend_pct * grinder_pct_list[0])
		grinder_pct_list[1] = int(blend_pct * grinder_pct_list[1])
		grinder_pct_list[2] = int(blend_pct * grinder_pct_list[2])
		return grinder_pct_list
	else:
		return grinder_pct_list
	
def main():
	blend_list = initData('blend')
	cust_list = initData('cust')
	coffeee_list = initData('coffee')
	computeCoffeeBlendSuggestion(blend_list,cust[1])
	
if __name__=='__main__':
	main()