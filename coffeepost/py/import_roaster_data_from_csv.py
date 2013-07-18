import csv
import MySQLdb
#import config as cfg

#db = MySQLdb.connect(user=cfg.user,passwd=cfg.pwd,db=cfg.db)
db = MySQLdb.connect(user='root',passwd='sct',db='coffeehouse')
cursor = db.cursor()


print 'rock n roll'
#filename = 'coffee-data.csv'
filename = 'coffee-roaster-data.csv'

csv_data = csv.reader(file(filename))
for row in csv_data:
	print row[0],row[1],row[2]
	f1 = """INSERT IGNORE INTO coffeez_roaster (roaster_name,city,image_url) VALUES ("%s","%s","%s")""" % (row[0],row[1],row[2])
	cursor.execute(f1)

db.commit()
cursor.close()
db.close()

print 'we have arrived. building secured. alpha tango'