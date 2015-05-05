#################################################
# CS 186 Final Project: Course Matching
# Harvard University
# 
# Yuechen Zhao <yuechenzhao@college.harvard.edu>
# Last Modified: May 3, 2015
# 
# Calculates metrics for comparing the different
# mechanisms
#################################################

from generate import Course, Student, generate
from hbs import hbs
from rds import rds
from copy import deepcopy
from ggplot import *
from pandas import DataFrame

print "Generating simulation data..."
courses, students = generate()

# RDS Mechanism
print "Copying simulation data for RDS Simulation..."
rds_courses = deepcopy(courses)
rds_students = deepcopy(students)
print "Running RDS Mechanism..."
rds(rds_courses, rds_students)

# HBS Mechanism
print "Copying simulation data for HBS Simulation..."
hbs_courses = deepcopy(courses)
hbs_students = deepcopy(students)
print "Running HBS Mechanism..."
hbs(hbs_courses, hbs_students)

# Calculate Metrics
mechanisms = ["RDS", "HBS"]

# percent of students matched with at least one course
rds_one_course = float(sum([1 if len(s.assigned) > 0 else 0 for s in rds_students])) / float(len(students))
hbs_one_course = sum([1 if len(s.assigned) > 0 else 0 for s in hbs_students]) / float(len(students))

df = DataFrame.from_dict({'mechanism': mechanisms, 'pct_students': [rds_one_course, hbs_one_course]})
print ggplot(df, aes(x = 'mechanism', y = 'pct_students')) + \
	geom_bar(stat = 'identity') + theme_bw() + \
	ggtitle("% Students Matched With >= 1 Course\n") + xlab("\nMechanism") + ylab("% of Students\n")

# percent of students who receive first choice course
rds_first_choice = float(sum([1 if len(s.assigned) > 0 and s.assigned[0] == s.preference[0] else 0 for s in rds_students])) / float(len(students))
hbs_first_choice = float(sum([1 if len(s.assigned) > 0 and s.assigned[0] == s.preference[0] else 0 for s in hbs_students])) / float(len(students))

df = DataFrame.from_dict({'mechanism': mechanisms, 'pct_students': [rds_first_choice, hbs_first_choice]})
print ggplot(df, aes(x = 'mechanism', y = 'pct_students')) + \
	geom_bar(stat = "identity") + theme_bw() + \
	ggtitle("% Students Matched With Top Choice\n") + xlab("\nMechanism") + ylab("% of Students\n")

# average rank of allotted courses
rds_sum_avg_rank = 0
for s in rds_students:
	if len(s.assigned) > 0:
		avg_rank = float(sum([s.preference.index(c) for c in s.assigned])) / float(len(s.assigned))
	else:
		avg_rank = s.threshold + 1
	rds_sum_avg_rank += avg_rank
rds_avg_rank = rds_sum_avg_rank / len(students)

hbs_sum_avg_rank = 0
for s in hbs_students:
	if len(s.assigned) > 0:
		avg_rank = float(sum([s.preference.index(c) for c in s.assigned])) / float(len(s.assigned))
	else:
		avg_rank = s.threshold + 1
	hbs_sum_avg_rank += avg_rank
hbs_avg_rank = hbs_sum_avg_rank / len(students)

df = DataFrame.from_dict({'mechanism': mechanisms, 'pct_students': [rds_avg_rank, hbs_avg_rank]})
print ggplot(df, aes(x = 'mechanism', y = 'pct_students')) + \
	geom_bar(stat = "identity") + theme_bw() + \
	ggtitle("Average Rank of Student's Courses\n") + xlab("\nMechanism") + ylab("Avg Rank\n")