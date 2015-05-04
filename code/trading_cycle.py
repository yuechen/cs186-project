# ==== TRADING PAIRS ====
# TWO POSSIBILITIES
# (1) student aims to obtain a specific course (* this is what I implemented *)
# (2) student aims to replace a specific course

# In my algorithm multiple trades might happen for a single student
# within the same trading round..?

# --- OBJECTS ---

# Course:
# 	id: starting from 0
# 	cap: int > 0 (GOOD DISTRIBUTION)
# 	desirability: from 0 to 1 → random
# 	preference: (list of student IDs) → random
#   assigned: list of tuples of (pref rank, student id), fav to least fav. initialize as empty list
#   num_assigned: int, initialize to zero 
#   requests: (list of tuples), initialize to empty list, representing the current requests in this round of DA (will empty after each round) 

# Student:
# 	id: starting from 0
#   preference: list of course IDs (highest preference at index 0). random from 0 to 1
# 	threshold: after which they do not want any of those courses, INCLUSIVE, so they don’t want the course at the index of the threshold: normal around 60, std 20
# 	assigned: list of course IDs that this student was assigned
#   num_assigned: int, initialize to zero 
#   next: int, initialize to zero, representing the next course student will proposition

# --- CODE ---

import random

# assuming these dictionaries are global variables
# (can alternately be passed around)
COURSE_DICT = None
STUDENT_DICT = None
NUM_ROUNDS = 500
NUM_CLASSES = 4
BLOCK_SIZE = 15

def swap_course(student, new_course, old_course):
	# add course
	student.assigned.append(new_course.id)
	new_rank = new_course.preference.index(student.id)
	new_course.assigned.append((new_rank, student.id))
	new_course.num_assigned += 1
	# remove course
	student.assigned.remove(old_course.id)
	old_rank = old_course.preference.index(student.id)
	old_course.assigned.remove((old_rank, student.id))
	old_course.num_assigned -= 1

# has to make the student better off AND not conflict with other blocks
def swappable(student, new_course, old_course):
	new_rank = student.preference.index(new_course.id)
	old_rank = student.preference.index(old_course.id)
	# student not better off (lower rank is more preferred)
	if new_rank >= old_rank:
		return False
	# course overlaps with another course
	for course_id in student.assigned:
		if course_id != old_course.id and course_id / BLOCK_SIZE == new_course.id / BLOCK_SIZE:
			return False
	return True

# s1 wants course with id s1_target_id from s2
# return TRUE if trade can occur, FALSE if not
def execute_trade(s1, s2, s1_target_id):
	for course_id in s1.assigned:
		s1_new_course = COURSE_DICT[s1_target_id]
		s2_new_course = COURSE_DICT[course_id]
		# check if valid trade
		if swappable(s1, s1_new_course, s2_new_course) and swappable(s2, s2_new_course, s1_new_course):
			swap_course(s1, s1_new_course, s2_new_course)
			swap_course(s2, s2_new_rank, s1_new_course)
			return True
	return False

# course is not always obtained (valid swap may not exist)
def obtain_course(student, course_id):
	target_course = COURSE_DICT[course_id]
	# no trade necessary (enough room)
	if target_course.num_assigned < target_course.cap:
		for trade_id in student.assigned:
			to_trade = COURSE_DICT[trade_id]
			if swappable(student, target_course, to_trade):
				swap_course(student, target_course, to_trade)
				return
	# trade necessary
	else:
		for _, other_id in target_course.assigned:
			other_student = STUDENT_DICT[other_id]
			if execute_trade(student, other_student, target_id):
				return

# student.next = next index in the PREFERENCE list (not next course id)
def trading_cycle():
	# initialize target course to most preferred course
	for student in STUDENT_DICT.values():
		student.next = 0
	# start trading
	for i in range(NUM_ROUNDS):
		# TODO: change this to random order?
		for student in STUDENT_DICT.values():
			# find next available preference if already owned
			while student.next in student.assigned:
				student.next += 1
			# continue only if target course is above threshold
			if student.next < student.threshold:
				course_id = student.preference[student.next]
				obtain_course(student, course_id)
				student.next += 1

def trading_cycle_matching(courses, student):
	# allocate courses randomly (with non-overlap category req)
	for student in STUDENT_DICT.values():
		blocks = set()
		while student.num_assigned < NUM_CLASSES:
			course = COURSE_DICT[random.choice(COURSE_DICT.keys())]
			if course.id / BLOCK_SIZE not in blocks and course.num_assigned < course.cap:
				blocks.add(course.id / BLOCK_SIZE)
				student.assigned.append(course.id)
				rank = course.preference.index(student.id)
				course.assigned.append((rank, student.id))
				course.num_assigned += 1
				student.num_assigned += 1
	# run trading cycle
	trading_cycle()