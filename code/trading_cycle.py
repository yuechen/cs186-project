# ==== TRADING PAIRS ====
# TWO POSSIBILITIES
# (1) student aims to obtain a specific course (* this is what I implemented *)
# (2) student aims to replace a specific course

# In my algorithm multiple trades might happen for a single student
# within the same trading round..?

# --- CODE ---

import random
from generate import Course, Student, generate, has_conflict
from operator import itemgetter
import numpy as np
from pprint import pprint
from copy import deepcopy

NUM_CLASSES = 4
BLOCK_SIZE = 15
NUM_SWAPS = 0
NUM_GRABS = 0

def swap_course(student, new_course, old_course):
	# add course
	student.assigned.append(new_course.ID)
	new_rank = new_course.preference.index(student.ID)
	new_course.assigned.append((new_rank, student.ID))
	new_course.num_assigned += 1
	# remove course
	student.assigned.remove(old_course.ID)
	old_rank = old_course.preference.index(student.ID)
	old_course.assigned.remove((old_rank, student.ID))
	old_course.num_assigned -= 1

# has to make the student better off AND not conflict with other blocks
def swappable(student, new_course, old_course):
	new_rank = student.preference.index(new_course.ID)
	old_rank = student.preference.index(old_course.ID)
	# student not better off (lower rank is more preferred)
	if new_rank >= old_rank:
		return False
	# course overlaps with another course
	for course_id in student.assigned:
		if course_id != old_course.ID and course_id / BLOCK_SIZE == new_course.ID / BLOCK_SIZE:
			return False
	return True

# s1 wants course with id s1_target_id from s2
# return TRUE if trade can occur, FALSE if not
def execute_trade(s1, s2, s1_target_id, course_dict):
	global NUM_SWAPS
	for course_id in s1.assigned:
		s1_new_course = course_dict[s1_target_id]
		s2_new_course = course_dict[course_id]
		# check if valid trade
		if swappable(s1, s1_new_course, s2_new_course) and swappable(s2, s2_new_course, s1_new_course):
			swap_course(s1, s1_new_course, s2_new_course)
			swap_course(s2, s2_new_course, s1_new_course)
			NUM_SWAPS += 1
			return True
	return False

# course is not always obtained (valid swap may not exist)
def obtain_course(student, course_id, student_dict, course_dict):
	global NUM_GRABS
	target_course = course_dict[course_id]
	# no trade necessary (enough room)
	if target_course.num_assigned < target_course.cap:
		for trade_id in student.assigned:
			to_trade = course_dict[trade_id]
			if swappable(student, target_course, to_trade):
				swap_course(student, target_course, to_trade)
				NUM_GRABS += 1
				return True
		return False
	# trade necessary
	else:
		for _, other_id in target_course.assigned:
			other_student = student_dict[other_id]
			if execute_trade(student, other_student, course_id, course_dict):
				return True
		return False

# student.next = next index in the PREFERENCE list (not next course id)
def trading_cycle(course_dict, student_dict, num_rounds = 100):
	global NUM_SWAPS, NUM_GRABS
	num_swaps = 0
	# initialize target course to most preferred course
	for student in student_dict:
		student.next = 0
	# start trading
	for i in range(num_rounds):
		# TODO: change this to random order?
		for student in student_dict:
			for j in range(len(course_dict)):
				if j not in student.assigned:
					swapped = obtain_course(student, j, student_dict, course_dict)
					if swapped:
						print "eyy", j, student.ID
						break
			# # print student.ID
			# # find next available preference if already owned
			# while student.next in student.assigned:
			# 	student.next += 1
			# # continue only if target course is above threshold
			# if student.next < student.threshold:
			# 	course_id = student.preference[student.next]
			# 	obtain_course(student, course_id, student_dict, course_dict)
			# 	student.next += 1
		print "yo", i
		print NUM_SWAPS, NUM_GRABS

def trading_cycle_matching(course_dict, student_dict):
	# allocate courses randomly (with non-overlap category req)
	for student in student_dict:
		blocks = set()
		while student.num_assigned < NUM_CLASSES:
			course = random.choice(course_dict)
			# print course.ID
			if course.ID / BLOCK_SIZE not in blocks and course.num_assigned < course.cap:
				blocks.add(course.ID / BLOCK_SIZE)
				student.assigned.append(course.ID)
				rank = course.preference.index(student.ID)
				course.assigned.append((rank, student.ID))
				course.num_assigned += 1
				student.num_assigned += 1
	# run trading cycle
	trading_cycle(course_dict, student_dict)

def main():
	print "Generating simulation data..."
	courses, students = generate(ncourses = 200, nstudents = 1000)
	trading_cycle_matching(courses, students)
	# print courses
	# print students

if __name__ == "__main__":
	main()