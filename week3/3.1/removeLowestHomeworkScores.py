import pymongo
import sys

connection = pymongo.Connection("mongodb://localhost", safe=True)


def removeLowestHomeworkScores():
	db = connection.school
	students = db.students
	
	# Find all the lowest scores per person first
	
	# tested to see if field can be a variable, which it can
	type = 'homework'
	query = ([{'$unwind':'$scores'},{'$match':{'scores.type':type}}, {'$group':{'_id':'$_id', 'min':{'$min':'$scores.score'}} }, {'$sort':{'_id':1}}])
	
	try:
		cursor = students.aggregate(query)
	
	except:
		print("Unexpected error"), sys.exc_info()[0]
	
	# doc now has an array of ids and lowest scores (called min - as specified in the query above)
	doc = cursor.get("result")
	for d in doc:
		print d
	
	# Get all the students
	allstudents = students.find()
	for s in allstudents:
		for d in doc:
			if d.get('_id') == s.get('_id'):
				print 'Going to remove ' + str(d.get('min')) + ' from ' + s.get('name')
				#students.remove({'$scores.score': {'$in': d.get('min')}})  <-- didn't work
				
				# Remove the lowest score from each student.  
				# $pull removes items from the array in the field named scores where type is homework and the score equals the min score
				students.update({'_id': d.get('_id')}, {'$pull': {'scores': {'type': 'homework', 'score': d.get('min')}}})
	
	

removeLowestHomeworkScores()