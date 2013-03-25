import serialHandle
import dbHandle
import jsonManager as jsonHandle
import tweetHandle
from datetime import datetime
import blendSuggestionCalculator as blendCalc
import json

blends = blendCalc.initData('blend')
cust1 = '{"body" : 5.0, "acidity":5.0, "fruity":1, "earthy":0, "chocolatey":0,"winey":1,"nutty":0,"herby":1,"smokey":0,"spicy":0,"floral":0}'
cust1 = json.loads(cust1)
blend_name = blendCalc.computeCoffeeBlendSuggestion(blends,cust1)

def getTheBlendDict(blend_name,blends):
     for each_dict in blends:
             if each_dict['name']==blend_name:
                     return each_dict
             else:
                     pass


blend_dict = getTheBlendDict(blend_name,blends)
aroma_dict = blendCalc.computeTop3Aromas(blend_dict)
aroma_json = jsonHandle.makerOfJsons(aroma_dict,'blend')
blend_chars_filename = '../www/data/dataout2.json'
jsonHandle.postJsonToServer(blend_chars_filename,aroma_json)