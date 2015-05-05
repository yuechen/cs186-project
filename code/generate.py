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
# Normal distribution with .85 probability drawing
# from X and .15 probability drawing from Y. 
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
	num_assigned = 0

	# for specific mechanisms
	assigned = []
	requests = []

	def __repr__(self):
		return "ID: " + str(self.ID) + ", Cap: " + str(self.cap) + ", Desirability: " + str(self.desirability) + ", Enrollment: " + str(self.num_assigned)

class Student:
	'''
	Describes one student in this simulation

	ID 			= 	the unique ID (int) for this student, indexed from 0
	preference 	= 	a list of course IDs, ordered by preference
	assigned 	= 	a list of course IDs, pecifies courses assigned to student
	threshold 	= 	the number of lotteried courses that the student actually want 
					(students can go for non-loterried courses)
	'''
	ID = None
	preference = None
	assigned = None
	threshold = None

	# for specific mechanisms
	num_assigned = 0
	requests = []
	next = 0
	groups_filled = []
	already_requested = []

	def __repr__(self):
		return "ID: " + str(self.ID) + ", Preference: " + str(self.preference) + ", Assigned: " + str(self.assigned) + ", Threshold: " + str(self.threshold)

def rand_cap():
	if np.random.binomial(1, 0.85, 1) == 1:
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

def has_conflict(course, others, ncourses = 320, ndivisions = 8):
	'''Make sure that ndivisions is a divisor of 120'''

	group_size = ncourses / ndivisions

	for c_other in others:
		if c_other / group_size == course / group_size:
			return True

	return False

def generate(ncourses = 320, nstudents = 6000):
	courses = []
	students = []

	for ID in range(ncourses):
		c = Course()
		c.ID = ID
		c.cap = rand_cap()
		c.desirability = np.random.uniform(0,1,1)[0]
		c.preference = range(nstudents)
		c.assigned = []
		shuffle(c.preference)
		courses.append(c)

	for ID in range(nstudents):
		s = Student()
		s.ID = ID
		s.threshold = rand_threshold()
		s.assigned = []

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