import MySQLdb as sql

def openDbConnection():
	"""instantiates the mysql db connection and returns the connection and cursor objects"""
	#abstract the user,passwd,db,host fields in a config file next
	connection = sql.connect(user="root",passwd="sct",db="sct")
	cursor = connection.cursor()
	return connection,cursor

def executeDbQuery(connection,cursor,query,query_type):
	"""executes the queries agains the database, query_type can be select or insert/update/delete"""
	if query_type =='select':
		cursor.execute(query)
		result = cursor.fetchall()
		return result
		
	elif query_type in ['insert','update','delete']:
		cursor.execute(query)
		connection.commit()
		#generate a log msg in the future
		
def closeDbConnection(connection,cursor):
	"""closes the cursor and database connections. Python does this automatically but you can explicitly call it."""
	cursor.close()
	connection.close()
		
if __name__=='__main__':
	main()
	
	'''
class MysqlDb(object):
	
	def __init__(self,database_type,user,passwd,db):
		self.database_type = database_type
		
	def openDbConnection(self):
	
	
	query = """Select customer_id,order_id,name,blend_name from Orders o join Blend using(blend_id)
	join Customer using(customer_id) order by o.time_created desc limit 1"""

	return int(result[0]),int(result[1]),str(result[2]),str(result[3])

	insert_query = """INSERT INTO Orders (order_id,customer_id,grinder0_pct,grinder1_pct,grinder2_pct,grind_complete) 
	VALUES (%d,%d,%s,%s,%s,'%s') ON DUPLICATE KEY UPDATE grinder0_pct=VALUES(grinder0_pct),grinder1_pct=VALUES(grinder1_pct),
	grinder2_pct=VALUES(grinder2_pct), grind_complete=VALUES(grind_complete)""" \
	% (order_id,customer_id,grinder_pct_list[0],grinder_pct_list[1],grinder_pct_list[2],time)
	'''