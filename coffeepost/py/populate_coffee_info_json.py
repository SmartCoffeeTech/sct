import MySQLdb as sql
import json
import subprocess
import config as cfg


def init_db():
	db = sql.connect(user=cfg.user,passwd=cfg.passwd,db=cfg.db)
	cursor = db.cursor()
	return db,cursor


def get_the_coffee_data(cursor):
	
	sql2 = """select c.id,roaster_name,coffee_name,origin from coffeez_coffee c join coffeez_roaster r \
	on c.roaster_id=r.id where binary_rep is not NULL"""
	cursor.execute(sql2)
	result = cursor.fetchall()
	
	coffee_dict = {}
	coffee_list = []
	
	for each in result:
		coffee_list.append({"roaster":each[1].replace("'",""),"coffee":each[2].replace("'",""), 
		"value":(each[1].replace("'","") + ", " + each[2].replace("'","")),
		"tokens":each[1].strip().replace("'","").split(" ")+each[2].strip().replace("'","").split(" ")+each[3].strip().replace("'","").split(" "),
		"idcof":int(each[0])
		})
		
		coffee_list.append({"roaster":each[1].replace("'","").encode('string_escape'),"coffee":each[2].replace("'","").encode('string_escape'),
		"value":(each[1].replace("'","").encode('string_escape') + ", " + each[2].replace("'","").encode('string_escape')),
		"tokens":each[1].strip().replace("'","").encode('string_escape').split(" ")+each[2].strip().replace("'","").encode('string_escape').split(" ")+each[3].strip().replace("'","").encode('string_escape').split(" "),
		"idcof":int(each[0])
		})
		
		
	print 'data is ok'
	
	return json.dumps(coffee_list)


def write_to_file(filename,data):
	f = open(filename,'wB+')
	f.write(data)
	f.close()


def main():
	try:
		filename = '/Users/kperko/work/sct/coffeepost/www/data/typeahead.json'
		#filename = '../data/typeahead1.json'
		db,cursor = init_db()
		print 'db initialized'
		
		data = get_the_coffee_data(cursor)
		print 'data gotten'
		
		write_to_file(filename,data)
		print 'file written'
		
		if subprocess.call(['chmod','755',filename])==0:
			print 'file permissions modified'
		else:
			print 'permission NOT modified'
	except Exception, e:
		print e
	

if __name__ == "__main__":
	main()
