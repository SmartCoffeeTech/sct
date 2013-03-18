import json

def getCoffeeJsons(roaster):
	try:
		if roaster==0:
			coffee_dict = {
					"roast_company": "Fourbarrel",
					"country_of_origin": "Ethiopia",
					"region": "Yukro",
					"farm": "Agaro",
					"varietal": "Heirloom",
					"altitude": "1900-2100 masl",
					"roast_date":'2013-02-20',
					"acidity": "6.2",
					"body": "7.5",
					"aroma1": "Fruity",
					"aroma2": "Chocolatey",
					"aroma3": "Herby",
					"farm_image1_url": "../img/fourbarrel_agaro_farm1.jpg",
					"farm_image2_url": "../img/fourbarrel_agaro_farm2.jpg",
					"farm_image3_url": "../img/fourbarrel_agaro_farm3.jpg",
					"roaster_image_url": "../img/fourbarrel.jpg"
				}
		elif roaster==1:
			coffee_dict = {
					"roast_company": "Ritual",
					"country_of_origin": "Colombia",
					"region": "Huila",
					"farm": "Desarrollo",
					"varietal": "Caturra",
					"altitude": "1500-1900 masl",
					"roast_date":'2013-02-14',
					"acidity": "6.2",
					"body": "7.5",
					"aroma1": "Fruity",
					"aroma2": "Chocolatey",
					"aroma3": "Herby",
					"farm_image1_url": "../img/ritual_desarrollo_farm1.jpg",
					"farm_image2_url": "../img/ritual_desarrollo_farm2.jpg",
					"farm_image3_url": "../img/ritual_desarrollo_farm3.jpg",
					"roaster_image_url": "../img/ritual.jpg"
				}
		elif roaster==2:
			coffee_dict = {
					"roast_company": "Sightglass",
					"country_of_origin": "Indonesia",
					"region": "Sulawesi",
					"farm": "Toarco",
					"varietal": "Typica",
					"altitude": "1400-2000 masl",
					"roast_date":'2013-02-19',
					"acidity": "6.2",
					"body": "7.5",
					"aroma1": "Fruity",
					"aroma2": "Chocolatey",
					"aroma3": "Herby",
					"farm_image1_url": "../img/sightglass_toarco_farm1.jpg",
					"farm_image2_url": "../img/sightglass_toarco_farm2.jpg",
					"farm_image3_url": "../img/sightglass_toarco_farm3.jpg",
					"roaster_image_url": "../img/sightglass.jpg"
				}
		else:
			raise Exception('Grinder value not recognized')
		return coffee_dict
	except Exception, e:
		print e

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

def makeJson(grinder_pct_list):
	# coffeeDict = dict(zip(coffee_list,grinder_pct_list))
	# coffeeDict = collections.OrderedDict(sorted(coffeeDict.items()))
	# coffeeDict["blendRecipe"]=blend_name
	coffeeDict["grinderPercentage0"]=grinder_pct_list[0]
	coffeeDict["grinderPercentage1"]=grinder_pct_list[1]
	coffeeDict["grinderPercentage2"]=grinder_pct_list[2]
	# coffeeDict["status"]='grinding'
	
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
					"farm_image1_url": "../img/",
					"farm_image2_url": "../img/",
					"farm_image3_url": "../img/",
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
	
def initJson(filename):
	setupjson = {
	       "status": "",
	       "canister": "",
	       "button": "",
	       "state": "",
	       "coffee":"",
	       "customer":"",
	       "blend":""
	}
	postJsonToServer(filename,setupjson)
	
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