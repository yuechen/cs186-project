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

MAX_CLASSES = 4
NUM_BLOCKS = 8
BLOCK_SIZE = 0
NUM_SWAPS = 0
NUM_GRABS = 0

def add_course(student, course):
	student.assigned.append(course.ID)
	rank = course.preference.index(student.ID)
	course.assigned.append((rank, student.ID))
	course.num_assigned += 1
	student.num_assigned += 1

def remove_course(student, course):
	student.assigned.remove(course.ID)
	rank = course.preference.index(student.ID)
	course.assigned.remove((rank, student.ID))
	course.num_assigned -= 1
	student.num_assigned -= 1

def swap_course(student, new_course, old_course):
	add_course(student, new_course)
	remove_course(student, old_course)

# has to make the student better off AND not conflict with other blocks
def swappable(student, new_course, old_course, combinatorial):
	if new_course.ID in student.assigned:
		return False
	if new_course.ID not in student.preference:
		new_rank = 10000 # undesirable
	else:
		new_rank = student.preference.index(new_course.ID)
	if old_course.ID not in student.preference:
		old_rank = 10000 # undesirable
	else:
		old_rank = student.preference.index(old_course.ID)
	# student not better off (lower rank is more preferred)
	if new_rank >= old_rank:
		return False
	# course overlaps with another course
	if combinatorial:
		for course_id in student.assigned:
			if course_id != old_course.ID and course_id / BLOCK_SIZE == new_course.ID / BLOCK_SIZE:
				return False
	return True

# s1 wants course with id s1_target_id from s2
# return TRUE if trade can occur, FALSE if not
def execute_trade(s1, s2, s1_target_id, course_dict, combinatorial):
	global NUM_SWAPS
	for course_id in s1.assigned:
		s1_new_course = course_dict[s1_target_id]
		s2_new_course = course_dict[course_id]
		# check if valid trade
		if swappable(s1, s1_new_course, s2_new_course, combinatorial) and swappable(s2, s2_new_course, s1_new_course, combinatorial):
			swap_course(s1, s1_new_course, s2_new_course)
			swap_course(s2, s2_new_course, s1_new_course)
			NUM_SWAPS += 1
			return True
	return False

# course is not always obtained (valid swap may not exist)
def obtain_course(student, course_id, student_dict, course_dict, combinatorial):
	global NUM_GRABS
	target_course = course_dict[course_id]
	# no trade necessary (enough room)
	if target_course.num_assigned < target_course.cap:
		if student.num_assigned < MAX_CLASSES:
			add_course(student, target_course)
			NUM_GRABS += 1
			return True
		else:
			for trade_id in student.assigned:
				to_trade = course_dict[trade_id]
				if swappable(student, target_course, to_trade, combinatorial):
					swap_course(student, target_course, to_trade)
					NUM_GRABS += 1
					return True
		return False
	# trade necessary
	else:
		for _, other_id in target_course.assigned:
			other_student = student_dict[other_id]
			if execute_trade(student, other_student, course_id, course_dict, combinatorial):
				return True
		return False

# student.next = next index in the PREFERENCE list (not next course id)
def trading_cycle(course_dict, student_dict, combinatorial, num_rounds = 6):
	global NUM_SWAPS, NUM_GRABS
	# start trading
	for i in range(num_rounds):
		# TODO: change this to random order?
		for student in student_dict:
			for course_id in student.preference:
				if course_id not in student.assigned:
					swapped = obtain_course(student, course_id, student_dict, course_dict, combinatorial)
					# stop searching for matching pair if course acquired or swapped
					if swapped:
						# print "ey", course_id, student.ID
						break
		print "=== ROUND", i, "===" 
		print "number of trades:", NUM_SWAPS
		print "number of classes acquired (no trade):", NUM_GRABS
		NUM_SWAPS = 0
		NUM_GRABS = 0

def drop_courses(course_dict, student_dict):
	dropped_courses = 0
	for student in student_dict:
		bad_ids = []
		for course_id in student.assigned:
			if course_id not in student.preference:
				bad_ids.append(course_id)
		for course_id in bad_ids:
			remove_course(student, course_dict[course_id])
			dropped_courses += 1
	return dropped_courses

def trading_cycle_matching(course_dict, student_dict, combinatorial = False):
	global BLOCK_SIZE
	BLOCK_SIZE = len(course_dict) / NUM_BLOCKS
	# allocate courses randomly (with non-overlap category req)
	for student in student_dict:
		blocks = set()
		num_classes = random.randint(0, 4)
		while student.num_assigned < num_classes:
			course = random.choice(course_dict)
			block_overlap = combinatorial and course.ID / BLOCK_SIZE in blocks
			if not block_overlap and course.ID not in student.assigned and course.num_assigned < course.cap:
				blocks.add(course.ID / BLOCK_SIZE)
				add_course(student, course)
	# run trading cycle
	print "start matching"
	trading_cycle(course_dict, student_dict, combinatorial)
	print "=== ROUNDS COMPLETE ==="
	# drop courses not within student preference threshold
	dropped_courses = drop_courses(course_dict, student_dict)
	print "number of courses dropped:", dropped_courses

def main():
	print "Generating simulation data..."
	courses, students = generate(ncourses = 120, nstudents = 1500)
	trading_cycle_matching(courses, students)

	# num_bugs = 0
	# for student in students:
	# 	if student.num_assigned == 0:
	# 		boolean = False
	# 		for course_id in student.preference:
	# 			if courses[course_id].cap > courses[course_id].num_assigned:
	# 				boolean = True
	# 		if boolean:
	# 			num_bugs += 1
	# # 	# print student.ID, student.assigned, student.preference
	# print "argh", num_bugs

if __name__ == "__main__":
	main()