#################################################
# CS 186 Final Project: Course Matching
# Harvard University
# 
# Yuechen Zhao <yuechenzhao@college.harvard.edu>
# Last Modified: May 3, 2015
# 
# HBS mechanism for course assignments where 
# there are lotteries.
#################################################

from generate import Course, Student, generate, has_conflict
from operator import itemgetter
import numpy as np
from pprint import pprint
from copy import deepcopy

def hbs(courses, students, nrounds = 4, combinatorial = False):
	ncourses = len(courses)
	nstudents = len(students)

	student_priorities = np.random.uniform(0, 1, nstudents)
	ids_priorities = zip(range(nstudents), student_priorities)
	ids_priorities = sorted(ids_priorities, key = itemgetter(1))

	preferences = [deepcopy(s.preference) for s in students]

	for r in range(nrounds):
		for (ID, priority) in ids_priorities:
			s = students[ID]

			if len(s.assigned) == 4:
				continue

			while(len(preferences[ID]) > 0):
				course_ID = preferences[ID].pop(0)
				course = courses[course_ID]
				if course.num_assigned < course.cap:
					if (combinatorial and (not has_conflict(course_ID, s.assigned))) or not combinatorial:
						s.assigned.append(course_ID)
						course.num_assigned += 1
						break

		ids_priorities = list(reversed(ids_priorities))