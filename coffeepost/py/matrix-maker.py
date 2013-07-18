import MySQLdb as mysql
#import config as cfg

def connect_to_db():
	#db = mysql.connect(user=cfg.user,passwd=cfg.passwd,db=cfg.db)
	db = mysql.connect(user="root",passwd="sct",db="coffeehouse")
	cursor = db.cursor()
	return db,cursor
	
	
def iterate_over_coffee_db(db,cursor):
	
	max_sql = '''select max(id) from coffeez_coffee'''
	cursor.execute(max_sql)
	result = cursor.fetchall()
	max_range = int(result[0][0])
	
	for each_id in xrange(1,max_range+1):
		sql = "select coffee_name,characteristics,binary_rep from coffeez_coffee where id=%d limit 1" % each_id
		cursor.execute(sql)
		result = cursor.fetchall()
		
		if len(result)>0 and result[0][2]==None:
			generate_coffee_vector(db,cursor,sql,each_id,result)

# get the keywords for their favorite coffee
def generate_coffee_vector(db,cursor,sql,each_id,result):
	
	#result object has name and characteristics
	coffee_name = result[0]
	coffee_keywords_string = result[0][1]
	coffee_keywords_list = coffee_keywords_string.split(',')
	coffee_keywords_list = [x.strip() for x in coffee_keywords_list]

	#get the matrix for all coffee flavors
	sql_CoffeeChars = "select classification,binary_rep,divisor from CoffeeChars"
	cursor.execute(sql_CoffeeChars)
	result = cursor.fetchall()
	
	# turn flavor matrix into a dict => class_name, binary_rep, divisor
	class_dict={}
	for each in result:
		class_dict[each[0]]=[each[1],int(each[2])]

	#pull out the appropriate binary for those flavors
	match_classification_list=[]
	binary_classification_list=[]

	#match the keys
	for each in coffee_keywords_list:
		if each in class_dict.keys():
			match_classification_list.append(each)
	
	if len(match_classification_list)>0:
	#create the list of binary values for each match
		for each in match_classification_list:
			binary_classification_list.append(int(class_dict[each][0],2))

	#turn binary rep into vector
		coffee_flavor_binary = bin(binary_classification_list[0])

		for each in binary_classification_list:
			coffee_flavor_binary = bin(int(coffee_flavor_binary,2) | each)

			coffee_flavor_vector = coffee_flavor_binary[2:]

	#insert that back into the database
		sql = '''update coffeez_coffee set binary_rep="%s" where id=%d''' % (coffee_flavor_vector,each_id)
		cursor.execute(sql)
		db.commit()
	else:
		return
	
	
def main():
	
	try:
		db,cursor = connect_to_db()
		iterate_over_coffee_db(db,cursor)
		print 'success'
		
	except Exception, e:
		print 'FUBAR: ',e
		
	finally:
		cursor.close()
		db.close()
		
if __name__ == '__main__':
	main()