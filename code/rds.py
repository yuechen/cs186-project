#################################################
# CS 186 Final Project: Course Matching
# Harvard University
# 
# Yuechen Zhao <yuechenzhao@college.harvard.edu>
# Last Modified: May 3, 2015
# 
# Random Serial Dictatorship method for
# course assignments where there are lotteries.
#################################################

from generate import Course, Student, generate, has_conflict
from operator import itemgetter, attrgetter
import numpy as np
from pprint import pprint
from random import shuffle

def rds(ncourses = 320, nstudents = 6000):
	courses, students = generate(ncourses, nstudents)

	shuffle(students)

	for s in students:
		for course_ID in s.preference:
			if len(s.assigned) == 4:
				break

			course = courses[course_ID]

			if (course.enrollment < course.cap) and (not has_conflict(course_ID, s.assigned)):
				s.assigned.append(course_ID)
				course.enrollment += 1

	students = sorted(students, key = attrgetter('ID'))

	return (courses, students)