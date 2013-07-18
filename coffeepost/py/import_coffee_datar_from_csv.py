import csv
import MySQLdb
import config as cfg

db = MySQLdb.connect(user='root',passwd='sct',db='coffeehouse')
cursor = db.cursor()

# filename='coffee-data.csv'
filename = 'coffee-data-info.csv'

csv_data = csv.reader(file(filename, 'rU'))
print 'read in csv'
try:
	a = csv_data.next()
except Exception, e:
	print 'EXCEPTION', e

try:
	for row in csv_data:
		f1 = """INSERT IGNORE INTO coffeez_coffee (roaster_id,roaster_link,coffee_name,roast_level,description,features,characteristics,acidity,origin) \
		 VALUES ((Select id from coffeez_roaster where roaster_name="%s"),"%s","%s","%s","%s","%s","%s","%s","%s")""" % \
		(row[0],row[1],MySQLdb.escape_string(row[2]),row[5],MySQLdb.escape_string(row[3]),MySQLdb.escape_string(row[4]),row[6],row[7],row[8])
		
		cursor.execute(f1)
except Exception, e:
	print e

#updated table
''' alter table coffeez_coffee add column binary_rep varchar(255) default null;
alter table coffeez_coffee add column divisor int default null;'''

db.commit()
cursor.close()
db.close()
print 'we have arrived. building secured. alpha tango charlie foxtrot'
