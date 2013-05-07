import MySQLdb as sql
import json
import subprocess


def init_db():
	# use config file for database on prod
	# db = mysql.connect(user=cfg.user, passwd=cfg.pass, db=cfg.db)
	db = sql.connect(user="root",passwd="sct",db="coffeehouse")
	cursor = db.cursor()
	return db,cursor


def get_the_coffee_data(cursor):
	
	sql2 = """select c.id,roaster_name,coffee_name,origin from coffeez_coffee c join coffeez_roaster r \
	on c.roaster_id=r.id where binary_rep is not NULL limit 10"""
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
	
	return json.dumps(coffee_list)


def write_to_file(filename,data):
	f = open(filename,'wB+')
	f.write(data)
	f.close()


def main():
	try:
		filename = '../www/data/coffee_json_db.json'
		db,cursor = init_db()
		data = get_the_coffee_data(cursor)
		write_to_file(filename,data)
		if subprocess.call(['chmod','755',filename])==0:
			print 'file permissions modified'
	except Exception, e:
		print e
	

if __name__ == "__main__":
	main()
