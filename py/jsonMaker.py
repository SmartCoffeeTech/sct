import json
import random
from time import sleep

def makeJson(blend_pct):
	coffeeDict = {
    "blendChoice": "Custom Control",
    "pulsePercentage": blend_pct,
    "grinder_1": "finished",
    "grinder_2": "",
    "grinder_3": ""
	}

	file = open('dataout1.json','w+')

	file.write(json.dumps(coffeeDict))

	file.close()

def main():
	for each in xrange(1,20):
		makeJson(each+5)
		print each
		sleep(5)
	

if __name__=='__main__':
	main()
