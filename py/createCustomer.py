import MySQLdb as sql
from datetime import datetime

def initDb():
	db = sql.connect(user="root",passwd="sct",db="sct")
	cursor = db.cursor()
	return db,cursor
	
def createCustomer(name,db_cur,db_con):
	msg = "INSERT INTO Customer (name) VALUES ('%s')" % name
	db_cur.execute(msg)
	db_con.commit()
	print "Created Customer %s | %s" % (name,datetime.now())
	

def main():
	name='Kevin' #get the name from the web service
	#when a new account gets created it should call the this function
	#or insert the name directly into the database (php)
	#php -> 
	db_con,db_cur = initDb()
	createCustomer(name,db_cur,db_con)	
	

if __name__=='__main__':
	main()