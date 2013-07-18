import numpy as np
from datetime import datetime
from operator import itemgetter, attrgetter
import json
import argparse
import os
import subprocess
from random import choice, shuffle
import config as cfg
os.environ['PYTHON_EGG_CACHE'] = '/tmp'

import MySQLdb as mysql



def init_db():
	
	db = mysql.connect(user=cfg.user, passwd=cfg.passwd, db=cfg.db)	
	cursor = db.cursor()
	return db,cursor


def get_customer_selection(cursor,cust_coffee_id):
		
	if cust_coffee_id != 0:
		sql = "select id,coffee_name,binary_rep from coffeez_coffee where id=%d limit 1" % cust_coffee_id
		
	elif cust_coffee_id == 0:
		# coffee_list = [1023,1010,1005,1000,984,989,992,997,993,998,1241,1243,1239,1057,1060,1068]
		coffee_list = [1,2]
		cust_coffee_id = choice(coffee_list)
		sql = "select id,coffee_name,binary_rep from coffeez_coffee where id=%d limit 1" % cust_coffee_id
        
	
	cursor.execute(sql)
	result = cursor.fetchall()
	
	#turn the result object into variables
	coffee_id = int(result[0][0])
	coffee_name = result[0][1]
	coffee_vector_string = result[0][2]
	#query the db for the selection
	return coffee_id,coffee_name,coffee_vector_string


def convert_string_to_list(string):
	
	generic_list = []
	
	for each_char in string:
		generic_list.append(each_char)
		
	return generic_list

	
def convert_string_to_np_array(string):
	#first convert the string to a list
	coffee_attribute_list = convert_string_to_list(string)
	#then convert the list to a numpy array
	#change dytpe to float to fix but does it still work?
	np_array = np.array(coffee_attribute_list, dtype=np.uint8)
	return np_array


def get_all_coffee_vectors(cust_coffee_id,cursor,for_sale):
	#from the db get the name and vector
	#convert these to np arrays
	#return coffee_vector
	
	sql_roast = "select roaster_id from coffeez_coffee where id=%d" % cust_coffee_id
	cursor.execute(sql_roast)
	result = cursor.fetchall()
	roaster_id = int(result[0][0])
	
	sql = "select id,coffee_name,binary_rep from coffeez_coffee where id!=%d and roaster_id!=%d and binary_rep is not NULL and for_sale=%d" % (cust_coffee_id,roaster_id,for_sale)
	#bring all the data into our matrix or create another function that does this
	sql2 = """select id,coffee_name,binary_rep,description,characteristics,origin,features,roaster_name from coffeez_coffee c join coffeez_roaster r on c.roaster_id=r.id
	where c.id!=%d and binary_rep is not NULL""" % cust_coffee_id
	cursor.execute(sql)
	result = cursor.fetchall()
	
	return result
	

def multiply_vectors(np_array,np_array_2):
	try:
		if type(np_array) == np.ndarray and type(np_array_2) == np.ndarray:
			return np_array*np_array_2
		else:
			raise Exception('your type is fucked up')
	except Exception, e:
		print e
		
		
def query_builder_rec_coffee(rec_coffee_id):
	get_rec_coffee_sql = '''select roaster_name as roast_company,coffee_name,cc.web_description as coffee_description,
	characteristics as coffee_aromas,cr.image_url as roast_image_url, cr.city as roast_location
	from coffeez_coffee cc join coffeez_roaster cr on cc.roaster_id=cr.id 
	where cc.id=%d
	limit 1;''' % rec_coffee_id
	
	return get_rec_coffee_sql
		
def query_db(cur,query):
	
	cur.execute(query)
	result = cur.fetchall()
	
	return result
		
	
def write_to_db(db,cur,base_coffee_id,coffee_id):
	#write the recommendation and create the Customer
	sql = """INSERT INTO Customer (customer_name,time_created) VALUES('',NOW())"""
	cur.execute(sql)
	db.commit()
	
	customer_id = int(cur.lastrowid)
	
	sql1 = """INSERT INTO Orders (customer_id,base_coffee_id,coffee_id,time_created) VALUES (%d,%d,%d,NOW())""" % (customer_id,base_coffee_id,coffee_id)
	cur.execute(sql1)
	db.commit()
	
	return customer_id
	
	
def write_to_json(filename,result_list,option):
	
	if option==1:
		json_dict = {}
		json_dict['coffee_id']=int(result_list[0])
		data = json.dumps(json_dict)
	else:
		data = json.dumps(result_list)
		
	with open(filename, 'w+b') as f:
		f.write(data)
		

def write_to_file(filename,arg1,arg2=None,arg3=None):
	
	if arg2==None:
		data = str([arg1])
		
	elif arg3==None:
		data = str([arg1,arg2])
	
	else:
		data = str([arg1,arg2,arg3])
	
	with open(filename, 'w+b') as f:
		f.write(data)
		

def compute_coffee_recommendation(np_coffee_array,coffee_tuple):
	
	unordered_cor_matrix_list = []
	rank_list = []
	
	for each in coffee_tuple:
		np_array = convert_string_to_np_array(each[2])

		correlation_matrix = multiply_vectors(np_coffee_array, np_array)
		unordered_cor_matrix_list.append(correlation_matrix)
		rank_list.append([each[0],each[1],correlation_matrix.sum(),each[2]])
		
	#sort the list by the number of matches
	
	rank_list = sort_correlation_matrix(rank_list)
	
	#top_5_cor_matrices = unordered_cor_matrix_list[-5:]
	#top_5_cor_values = rank_list[:5]
	
	data = rank_list[:1][0][0:3]
	rec_coffee_vector = rank_list[:1][0][3]
	rec_coffee_id = int(data[0])
	
	return data,rec_coffee_id,rec_coffee_vector
	
def sort_correlation_matrix(rank_list):
	
	pretty_rank_list = []
	
	rank_list.sort(key=itemgetter(2), reverse=True)
	
	for each in rank_list:
		if each[2]>0:
			pretty_rank_list.append(each)
			
		
	rank_list = rank_list[:3]
	shuffle(pretty_rank_list)
	
	return pretty_rank_list
	
	
def parse_result(raw_datars,coffee_aroma_string):
	
	parse_dict = {
	'roast_company' : str(raw_datars[0]),
	'coffee_name' : str(raw_datars[1]),
	'coffee_description' : str(raw_datars[2]),
	'coffee_aromas' : coffee_aroma_string,
	'roast_image_url' : str(raw_datars[4]),
	'roast_location' : str(raw_datars[5])
	}
	
	return parse_dict
	

def compute_coffee_aroma_matches(coffee_vector_string,rec_coffee_vector):
	
	#where a and b are numpy vectors
	coffee_attribute_list = convert_string_to_list(coffee_vector_string)
	coffee_attribute_list2 = convert_string_to_list(rec_coffee_vector)
	
	np_array = np.array(coffee_attribute_list, dtype=np.uint8)
	np_array2 = np.array(coffee_attribute_list2, dtype=np.uint8)

	np_array3 = np_array+np_array2
	np_array3 = np_array3+np_array2
	sum_coffee_vector_string = ','.join(['%d' % num for num in np_array3])
	sum_coffee_vector_string = sum_coffee_vector_string.replace(",","")
	
	return sum_coffee_vector_string
	
	
def compute_coffee_aromas_from_bin(sum_coffee_vector_string):
	
	att_list = ["banana","lychee","guava","apricot","melon","nectarine","pineapple","cranberry","raspberry","strawberry","redcurrant","cherry","plum","blackberry","blueberry","blackcurrant","apple","goosberry","pear","grapefruit","tangerine","clementine","mandarin","lime","grape","peach","orange","lemon","tropical fruit","stone fruit","berry","citrus","fruity","zesty","fruity","tobacco","tea ","coffee blossom","orange blossom","acacia","honeysuckle","chamomile","elderflower","geranium","fragrent","rose","violet","iris","leafy","floral","flowery","cardamon","caraway","coriander","thyme","eucalyptus","lavender","fennel","coconut","peanuts","walnuts","hazelnut","almond","ginger","nutmeg","clove","licorice","juniper","nutty ","grassy","minty","onion","garlic","nutty ","herby","cucumber","peas","hay ","tomato","potato","asparagus","malty","balsamic","honey","maple","cedar","piney","toast","carbony","ashy","tarry","charred","burnt","sour","soury","acrid","winey","tangy","nippy","creamy","milk chocolate","bittersweet chocolate","dark chocolate","cocoa","sugar","vanilla","chocolate","cinnamon","caramel","pepper","syrupy","spicy","smokey","sweet","buttery","smooth","salty","tart","earthy","candy"]

	binary_rep = sum_coffee_vector_string
	binary_rep = binary_rep[1:]
	binary_rep_num_atts = binary_rep.count('2')

	matched_att_list = []

	for i,c in enumerate(binary_rep):
		if "2"==c:
			matched_att_list.append(att_list[i])
		elif "3"==c:
			matched_att_list.append(att_list[i]+"*")


	matched_att_list = list(set(matched_att_list))
	str_matched_att_list = ", ".join(matched_att_list)

	return str_matched_att_list
	


def main():
	
	try:
		#hard_coded - set to 0 for testing
		for_sale=1
		
		parser = argparse.ArgumentParser(description='Process some command line args. Imagine that!')
		parser.add_argument('-id', '--coffee-id', type=int, help='the coffee_id in the db')
		parser.add_argument('-t', '--epoch-time', type=int, help='time since epoch')
	
		#parse args and assign vars
		args = parser.parse_args()
		cust_coffee_id = args.coffee_id
		epoch_time = args.epoch_time
		
		#TESTING
		cust_coffee_id = 1
		epoch_time = 1399
		
		#setup fn
		filename = '/Users/kperko/work/sct/coffeepost/www/data/customer_rec' + str(epoch_time) + '.json'
		recommended_json_filename = '/Users/kperko/work/sct/coffeepost/www/data/dataout' + str(epoch_time) + '.json'
		filename_2 = '/Users/kperko/work/sct/coffeepost/www/data/recinfo' + str(epoch_time)
		log_file =   '/Users/kperko/work/sct/coffeepost/www/data/devlog'

		#setup db
		db,cur = init_db()
	
		#setup coffee rec
		coffee_id,coffee_name,coffee_vector_string = get_customer_selection(cur,cust_coffee_id)
		#print coffee_vector_string
		print 'get_customer_selection finished'
		
		np_coffee_array = convert_string_to_np_array(coffee_vector_string)
		#print np_coffee_array
		print 'convert_string_to_np_array finished'
		
		coffee_tuple = get_all_coffee_vectors(coffee_id,cur,for_sale)
		#print coffee_tuple
		print 'get_all_coffee_vectors finished'
	
		data,rec_coffee_id,rec_coffee_vector = compute_coffee_recommendation(np_coffee_array,coffee_tuple)
		#print 'compute_coffee_recommendation finished'
		
		#ADD THIS FN
		sum_coffee_vector_string = compute_coffee_aroma_matches(coffee_vector_string,rec_coffee_vector)
		#print 'sum_coffee_vector_string: ', sum_coffee_vector_string
		coffee_aroma_string = compute_coffee_aromas_from_bin(sum_coffee_vector_string)
		print 'coffee_aroma_string: ', coffee_aroma_string
		
		query = query_builder_rec_coffee(rec_coffee_id)
		result = query_db(cur,query)
		result = result[0]
		parsed_result_dict = parse_result(result,coffee_aroma_string)
	
		write_to_json(filename,data,1)
		print 'wrote:', filename
		
		write_to_json(recommended_json_filename,parsed_result_dict,0)
		#print 'wrote json: ', recommended_json_filename
		
		customer_id = str(write_to_db(db,cur,cust_coffee_id,rec_coffee_id))
		#print 'customer_id: ', customer_id
		# epoch_time = str(epoch_time)
	
		#needed?
		subprocess.call(["chmod", "755", filename])
		write_to_file(filename_2,epoch_time)
		#print 'wrote final file: ', filename_2
		
		success = 'p3rk0 successfully generated your coffee rec'
		print success
		
	except Exception, e:
		dateval = str(datetime.today())
		print(log_file,dateval,str(e))
		write_to_file(log_file,dateval,str(e))
		
		
	finally:
		cur.close()
		db.close()
		if 'success' in locals():
			print 'script finished'
		else:
			print 'script failed'
	
	
if __name__ == "__main__":
	main()