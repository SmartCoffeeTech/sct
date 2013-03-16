import json

def makerOfJsons(dictr,section):
	prep_dict={}
	prep_dict[section] = dictr
	json_blob = json.dumps(prep_dict)
	
 	return json_blob

def updaterOfJsons(filename,section,dictr):
	'''read json objects from the server,update and save changes to server'''
	file = open(filename,'r+b')
	coffeeDict = json.loads(file.readline())
	coffeeDict[section]=dictr
	jsonData = json.dumps(coffeeDict)
	
	#pointer to the beginning of the file
	file.seek(0)
	file.truncate()
    #now update and close the file
	file.write(jsonData)
	file.close()

def makeJson(coffee_list,grinder_pct_list,blend_name,page):
	coffeeDict =  dict(zip(coffee_list,grinder_pct_list))
	coffeeDict = collections.OrderedDict(sorted(coffeeDict.items()))
	coffeeDict["blendRecipe"]=blend_name
	coffeeDict["grinderPercentage0"]=grinder_pct_list[0]
	coffeeDict["grinderPercentage1"]=grinder_pct_list[1]
	coffeeDict["grinderPercentage2"]=grinder_pct_list[2]
	coffeeDict["status"]='grinding'
	
	#base selection page - produced for base_blend.html
	if page=='base_blend.html':
		overall = {}
		base_blend = {}
		base_blend['acidity']=val
		base_blend['body']=val
		base_blend['aroma1']=val
		base_blend['aroma2']=val
		base_blend['aroma3']=val
	
		overall['base_blend']=base_blend
	
	overall['coffee']=coffeeDict
	
	coffeeDictJson = json.dumps(coffeeDict)
	return coffeeDictJson
	
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
	
'''	
		{
			"status": "grinding",
			"canister": "false",
			"state":"base",
			"coffee":
				{
					"roast_company": "Ritual Roasters",
					"country_of_origin": "Colombia",
					"region": "Some region",
					"farm": "Little Farm",
					"varietal": "Typica",
					"altitude": "1000 masl",
					"acidity": "6.2",
					"body": "7.5",
					"aroma1": "Fruity",
					"aroma2": "Chocolatey",
					"aroma3": "Herby",
					"farm_image1_url": "1001",
					"farm_image2_url": "1002",
					"farm_image3_url": "1003",
					"roaster_image_url": "img/fourbarrel.jpg"
				},
			"customer":
				{
					"acidity": "8",
					"body": "9",
					"aroma1": "Fruity",
					"aroma2": "Chocolatey",
					"aroma3": "Herby",
					"grinder0Percentage": 40,
					"grinder1Percentage": 0,
					"grinder2Percentage": 0,
					"name": "Erik"
				},
			"blend":
			{
				"grinder0Percentage":40,
				"grinder1Percentage":30,
				"grinder2Percentage":0,
				"aroma1":"honey",
				"aroma2":"cherry",
				"aroma3":"winning"
			}
		}
	'''
	
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
	
def readJson(filename):
	file = open(filename,'r+b')
	jsonDict = {}
	jsonDict = json.loads(file.readline())
	return jsonDict
	file.close()
	
def resetJsonFile(filename):
	file = open(filename,'w+')
	file.close()
	
def postJsonToServer(filename,coffeeDictJson):
	file = open(filename,'w+')
	file.write(coffeeDictJson)
	file.close()