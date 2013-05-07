import numpy as np
import MySQLdb as mysql
from operator import itemgetter, attrgetter
import json
import argparse
import os
import subprocess
import config as cfg
#make sure __init__.py is in dir


def init_db():
	# use config file for database on prod
	db = mysql.connect(user=cfg.user, passwd=cfg.passwd, db=cfg.db)	
	cursor = db.cursor()
	return db,cursor


def get_customer_selection(cursor,cust_coffee_id):
	#hard code the id to test the recommender
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


def get_all_coffee_vectors(cust_coffee_id,cursor):
	#from the db get the name and vector
	#convert these to np arrays
	#return coffee_vector
	sql = "select id,coffee_name,binary_rep from coffeez_coffee where id!=%d and binary_rep is not NULL" % cust_coffee_id
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
	

def emit_top_5_results(db,cur,top_5_result_list,filename='null',destination='null'):
	pass
	if destination == 'db':
		write_to_db(db,cur,top_5_result_list)
	elif destination  == 'json':
		write_to_json(filename,top_5_result_list)
	else:
		print top_5_result_list
		
	
def write_to_db(db,cur,coffee_id):
	#write the recommendation and create the Customer
	sql = """INSERT INTO Customer (name) VALUES('')"""
	cur.execute(sql)
	db.commit()
	
	customer_id = int(cursor.lastrowid)
	
	sql1 = """INSERT INTO Orders (customer_id,coffee_id) VALUES (%d,%d)""" % (customer_id,coffee_id)
	cur.execute(sql1)
	db.commit()
	
	
def write_to_json(filename,result_list):
	json_dict = {}
	json_dict['coffee_id']=int(result_list[0][0])
	
	data = json.dumps(json_dict)
	with open(filename, 'w+b') as f:
		f.write(data)
		

def compute_coffee_recommendation(coffee_tuple):
	
	unordered_cor_matrix_list = []
	rank_list = []
	
	for each in coffee_tuple:
		np_array = convert_string_to_np_array(each[2])

		correlation_matrix = multiply_vectors(np_coffee_array, np_array)
		unordered_cor_matrix_list.append(correlation_matrix)
		rank_list.append([each[0],each[1],correlation_matrix.sum()])
		
	#sort the list by the number of matches
	rank_list.sort(key=itemgetter(2), reverse=True)
	
	top_5_cor_matrices = unordered_cor_matrix_list[-5:]
	top_5_cor_values = rank_list[:5]
	data = rank_list[:1]
	
	rec_coffee_id = int(data[0][0])
	
	return data,rec_coffee_id


def main():
	#from coffee_recommendation_generator import *
	#import numpy as np
	#import MySQLdb as mysql
	
	#setup arg parsing
	parser = argparse.ArgumentParser(description='Process some command line args. Imagine that!')
	parser.add_argument('-id', '--coffee-id', type=int, help='the coffee_id in the db')
	parser.add_argument('-t', '--time-epoch', type=int, help='time since epoch')
	
	#parse args and assign vars
	args = parser.parse_args()
	cust_coffee_id = args.coffee_id
	time_epoch = args.time_epoch
	
	#setup fn
	filename = '/tmp/customer_rec' + str(time_epoch) +'.json'

	#setup db
	db,cur = init_db()
	
	#setup coffee rec
	coffee_id,coffee_name,coffee_vector_string = get_customer_selection(cur,cust_coffee_id)
	np_coffee_array = convert_string_to_np_array(coffee_vector_string)
	coffee_tuple = get_all_coffee_vectors(cust_coffee_id,cur)
	
	data,rec_coffee_id = compute_coffee_recommendation(coffee_tuple)
	
	write_to_json(filename,data)
	write_to_db(db,cur,rec_coffee_id)
	
	time_epoch = str(time_epoch)
	subprocess.call(["chmod", "755", filename])
	subprocess.call(["php", "customer_redirect.php", "-t", time_epoch])
	
	
if __name__=='__main__':
	main()