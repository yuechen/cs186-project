####################################################
# CS 186 Final Project: Course Matching
# Harvard University
# 
# Yuechen Zhao <yuechenzhao@college.harvard.edu>
# Last Modified: May 3, 2015
#
# generate() returns a tuple of two two lists.
# The first is a list of Student objects,
# and the second is a list of Course objects.
#
# The capacity for courses is distributed as a mixed
# Normal distribution with .7 probability drawing
# from X and .3 probability drawing from Y. 
# X ~ N(20, 5) and Y ~ N(100, 30)
# All capacities are forced to be > 0. If any is
# <= 0, then the capacity is redrawn from the
# distribution.
#
# The threshold for course preferences for students
# is distributed ~ N(4, 2). If a negative number is
# drawn from the distribution, then it is discarded
# and another number is drawn.
#
# Students' preferences for courses are drawn from
# courses by desirability. That is, the most
# preferred course for any student is drawn from the
# weighted list of IDs (weighted by desirability).
# Then the second is drawn from the remaining 
# (no replacement), etc.
#####################################################

import numpy as np
from random import shuffle
from pprint import pprint

class Course:
	'''
	Describes one course in this simulation

	ID 				= 	the unique ID (int) for this course, indexed from 0
	cap				= 	the capacity (int) for this course
	desirability	= 	a desirability factor (from 0 to 1) for this course
						0 is highly undesirable. 1 is highly desirable.
	preference 		= 	a list of student IDs, ordered by preference
	'''
	ID = None
	cap = None
	desirability = None
	preference = None

	def __repr__(self):
		return "ID: " + str(self.ID) + ", Cap: " + str(self.cap) + ", Desirability: " + str(self.desirability) + ", Preference: " + str(self.preference)

class Student:
	'''
	Describes one student in this simulation

	ID 			= 	the unique ID (int) for this student, indexed from 0
	preference 	= 	a list of course IDs, ordered by preference
	assigned 	= 	a list of course IDs, pecifies courses assigned to student
	threshold 	= 	the position in the preference list that states the LAST 
					course the student would want. After the course in this
					position, the student would rather go for non-lotteried
					courses.
	'''
	ID = None
	preference = None
	assigned = None
	threshold = None

	def __repr__(self):
		return "ID: " + str(self.ID) + ", Preference: " + str(self.preference) + ", Assigned: " + str(self.assigned) + ", Threshold: " + str(self.threshold)

def rand_cap():
	if np.random.binomial(1, 0.7, 1) == 1:
		cap = int(round(np.random.normal(20, 5, 1)[0]))
	else:
		cap = int(round(np.random.normal(100, 30, 1)[0]))

	if cap < 0:
		return rand_cap()
	else:
		return cap

def rand_threshold():
	threshold = int(round(np.random.normal(4, 2, 1)[0]))
	if threshold < 0:
		return rand_threshold()
	else:
		return threshold

def generate(ncourses = 120, nstudents = 6000):
	courses = []
	students = []

	for ID in range(ncourses):
		c = Course()
		c.ID = ID
		c.cap = rand_cap()
		c.desirability = np.random.uniform(0,1,1)[0]
		c.preference = range(nstudents)
		shuffle(c.preference)
		courses.append(c)

	for ID in range(nstudents):
		s = Student()
		s.ID = ID
		s.threshold = rand_threshold()

		course_ids = list(range(ncourses))
		probs = [c.desirability for c in courses]
		total = sum(probs)
		probs = map(lambda x: x / total, probs)
		s.preference = []

		for k in range(s.threshold):
			p = np.random.choice(course_ids, 1, probs)[0]
			i = course_ids.index(p)
			course_ids.pop(i)
			probs.pop(i)
			s.preference.append(p)

		students.append(s)

	return (courses, students)