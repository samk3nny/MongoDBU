import pymongo
import sys

# establish a connection to the database
connection = pymongo.Connection("mongodb://localhost", safe=True)

def find_homework():
	print('Finding all homeworks')
	query = {'type':'homework'}
	
	db = connection.students
	grades = db.grades
	
	try:
		cursor = grades.find(query)
		cursor = cursor.sort([('student_id', pymongo.DESCENDING),('score',pymongo.DESCENDING)])
		
		previous_score = 0
		previous_student = 0
		counter = 0
		for doc in cursor:			
			current_score = doc['score']
			current_student = doc['student_id']
			if current_student == previous_student:
				if current_score < previous_score :
					counter += 1								
					print doc
					grades.remove(doc)

			previous_score = doc['score']
			previous_student = doc['student_id']
		print('counter: ' + str(counter))

	except:
		print "Unexpected error:", sys.exc_info()[0]
		raise

find_homework()