import json

def makeJson(coffee_list,grinder_pct_list,blend_name):
	coffeeDict =  dict(zip(coffee_list,grinder_pct_list))
	coffeeDict = collections.OrderedDict(sorted(coffeeDict.items()))
	coffeeDict["blendRecipe"]=blend_name
	coffeeDict["grinderPercentage0"]=grinder_pct_list[0]
	coffeeDict["grinderPercentage1"]=grinder_pct_list[1]
	coffeeDict["grinderPercentage2"]=grinder_pct_list[2]
	coffeeDict["status"]='grinding'
	
	'''
	coffeeDict = {
    "blendRecipe": blend_name,
    "grinderPercentage0": grinder_pct_list[0],
	"grinderPercentage1": grinder_pct_list[1],
	"grinderPercentage2": grinder_pct_list[2],
	coffee_list[0]: grinder_pct_list[0],
	coffee_list[1]: grinder_pct_list[1],
	coffee_list[2]: grinder_pct_list[2],
	"status":'grinding'
	}
	'''
	coffeeDictJson = json.dumps(coffeeDict)
	return coffeeDictJson
	
def updateJson(filename,status):
	file = open(filename,'r+b')
	coffeeDict = json.loads(file.readline())
	coffeeDict['status']=status
	jsonData = json.dumps(coffeeDict)
	
	#pointer to the beginning of the file
	file.seek(0)
	file.truncate()
    #now update and close the file
	file.write(jsonData)
	file.close()
	
def resetJsonFile(filename):
	file = open(filename,'w+')
	file.close()
	
def postJsonToServer(filename,coffeeDictJson):
	file = open(filename,'w+')
	file.write(coffeeDictJson)
	file.close()