import pymongo
import bson
import sys

connection = pymongo.Connection("mongodb://localhost", safe=True)

db=connection.school
students = db.students
   
def test():
	query = ([{'$unwind':'$scores'},{'$group':{'_id':'$_id', 'average':{'$avg':'$scores.score'}}}, {'$sort':{'average':-1}}, {'$limit':1}])
	
	try:
		cursor = students.aggregate(query)
		
	except:
		print("Unexpected error"), sys.exc_info()[0]
	
	doc = cursor.get("result")
	print doc[0].get("_id")
	
test()