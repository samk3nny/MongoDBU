import pymongo
import sys

connection = pymongo.Connection("mongodb://localhost", safe=True)

def listScores():
	db = connection.school
	students = db.students
	#query = ({'scores.type':'homework'}, {'_id':0})
	#query = ([ { '$group': { 'name':'Rae Kohout', 'lowestHW': { '$min': '$score'} } } ])
	#query = ( {'$unwind':'$scores'},{'$match':{'scores.type':'homework'}}, {'$sort':{'name':1}})
	query = ( {'$unwind':'$scores'}, {'$match':{'scores.type':'homework'}}, {'$group':{'_id':'$_id', 'scores':{'$push':'$scores'}}}, {'$sort':{'_id':1}})
	
	try:
		cursor = students.aggregate(query)
		#cursor = students.find(query)
		#cursor = cursor.sort([('_id', pymongo.DESCENDING)])
	
	except:
		print("Unexpected error"), sys.exc_info()[0]
		
	doc = cursor.get("result")
	
	for d in doc:
		print str(d.get('_id')) + ' There are ' + str(len(d.items())) + ' elements in ' + str(d)
		
	

listScores()