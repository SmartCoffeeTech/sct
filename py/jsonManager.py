import json

def getCoffeeJsons(grinder):
	try:
		if grinder==0:
			coffee_dict = {
					"roast_company": "Fourbarrel",
					"country_of_origin": "Ethiopia",
					"region": "Yukro",
					"farm": "Agaro",
					"varietal": "Heirloom",
					"altitude": "1900-2100 masl",
					"roast_date":"2013-02-20",
					"acidity": 10,
					"body": 7,
					"aroma1": "Fruity",
					"aroma2": "Nutty",
					"aroma3": "Chocolatey",
					"farm_image1_url": "img/ethiopia_map.gif",
					"farm_image2_url": "img/ethiopia_farm.jpg",
					"farm_image3_url": "img/ethiopia_flag.gif",
					"roaster_image_url": "img/fourbarrel.jpg"
				}
		elif grinder==1:
			coffee_dict = {
					"roast_company": "Ritual",
					"country_of_origin": "Bolivia",
					"region": "Caranavi",
					"farm": "Calama",
					"varietal": "Caturra, Catuai, Typica",
					"altitude": "1350 masl",
					"roast_date":"2013-02-19",
					"acidity": 5,
					"body": 3,
					"aroma1": "Nutty",
					"aroma2": "Chocolatey",
					"aroma3": "Herby",
					"farm_image1_url": "img/bolivia_map.gif",
					"farm_image2_url": "img/bolivia_farm.jpg",
					"farm_image3_url": "img/bolivia_flag.gif",
					"roaster_image_url": "img/ritual.gif"
				}
		elif grinder==2:
			coffee_dict = {
					"roast_company": "Sightglass",
					"country_of_origin": "Indonesia",
					"region": "Sulawesi",
					"farm": "Toarco",
					"varietal": "Typica",
					"altitude": "1400-2000 masl",
					"roast_date":"2013-02-19",
					"acidity": 1,
					"body": 10,
					"aroma1": "Earthy",
					"aroma2": "Fruity",
					"aroma3": "Floral",
					"farm_image1_url": "img/indonesia_map.gif",
					"farm_image2_url": "img/indonesia_farm.jpg",
					"farm_image3_url": "img/indonesia_flag.gif",
					"roaster_image_url": "img/sightglass.png"
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
	coffeeDict={}
	# coffeeDict = dict(zip(coffee_list,grinder_pct_list))
	# coffeeDict = collections.OrderedDict(sorted(coffeeDict.items()))
	# coffeeDict["blendRecipe"]=blend_name
	coffeeDict["grinder0Percentage"]=grinder_pct_list[0]
	coffeeDict["grinder1Percentage"]=grinder_pct_list[1]
	coffeeDict["grinder2Percentage"]=grinder_pct_list[2]
	
	return coffeeDict
	
def initJson(filename):
	setupjson = {
	       "status": "",
	       "canister": "",
	       "button": "",
	       "state": "",
	       "coffee":"",
		   "customerPercentages":"",
		   "blendPercentages":"",
		   "blendAromas":""
	}
	
	setupjson = json.dumps(setupjson)
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