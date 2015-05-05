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
from DA import deferred
from trading_cycle import trading_cycle_matching

print "Generating simulation data..."
courses, students = generate()

def bar_graph(df, title):
	return ggplot(df, aes(x = 'mechanism', y = 'pct_students')) + \
	geom_bar(stat = 'identity') + theme_bw() + \
	ggtitle(title) + xlab("\nMechanism") + ylab("% of Students\n")

def sublist(l, indicies):
	return [l[i] for i in indicies]

si_courses = []
si_students = []

ncourses = len(courses)
nstudents = len(students)

mechanisms = ["RDS", "RDS Combinatorial", "HBS", "HBS Combinatorial", "DA RSP", "DA RSP Combinatorial", "DA TSP", "DA TSP Combinatorial", "Trading", "Trading Combinatorial"]

# RDS Mechanism
print "Copying simulation data for RDS Simulation..."
si_courses.append(deepcopy(courses))
si_students.append(deepcopy(students))
print "Running RDS Mechanism..."
rds(si_courses[0], si_students[0])

# RDS Mechanism, Combinatorial
print "Copying simulation data for RDS Combinatorial Simulation..."
si_courses.append(deepcopy(courses))
si_students.append(deepcopy(students))
print "Running RDS Combinatorial Mechanism..."
rds(si_courses[1], si_students[1], combinatorial = True)

# HBS Mechanism
print "Copying simulation data for HBS Simulation..."
si_courses.append(deepcopy(courses))
si_students.append(deepcopy(students))
print "Running HBS Mechanism..."
hbs(si_courses[2], si_students[2])

# HBS Mechanism, Combinatorial
print "Copying simulation data for HBS Combinatorial Simulation..."
si_courses.append(deepcopy(courses))
si_students.append(deepcopy(students))
print "Running HBS Combinatorial Mechanism..."
hbs(si_courses[3], si_students[3], combinatorial = True)

# DA Mechanism Random Student Preferences, Non-Combinatorial
print "Copying simulation data for DA Random Student Preferences Non-Combinatorial Simulation..."
si_courses.append(deepcopy(courses))
si_students.append(deepcopy(students))
print "Running DA RSP Non-Combinatorial Simulation..."
deferred(si_courses[4], si_students[4])

# DA Mechanism Random Student Preferences, Combinatorial
print "Copying simulation data for DA Random Student Preferences Combinatorial Simulation..."
si_courses.append(deepcopy(courses))
si_students.append(deepcopy(students))
print "Running DA RSP Combinatorial Simulation..."
deferred(si_courses[5], si_students[5], combinatorial = True)

# DA Mechanism Tiered Student Preferences, Non-Combinatorial
print "Copying simulation data for DA Tiered Student Preferences Non-Combinatorial Simulation..."
si_courses.append(deepcopy(courses))
si_students.append(deepcopy(students))
print "Running DA TSP Non-Combinatorial Simulation..."
deferred(si_courses[6], si_students[6], tiered = True)

# DA Mechanism Tiered Student Preferences, Combinatorial
print "Copying simulation data for DA Tiered Student Preferences Combinatorial Simulation..."
si_courses.append(deepcopy(courses))
si_students.append(deepcopy(students))
print "Running DA TSP Combinatorial Simulation..."
deferred(si_courses[7], si_students[7], tiered = True, combinatorial = True)
'''
# Trading Mechanism, Non-Combinatorial
print "Copying simulation data for Trading Non-Combinatorial Simulation..."
si_courses.append(deepcopy(courses))
si_students.append(deepcopy(students))
print "Running Trading Non-Combinatorial Simulation..."
trading_cycle_matching(si_courses[8], si_students[8])

# Trading Mechanism, Combinatorial
print "Copying simulation data for Trading Combinatorial Simulation..."
si_courses.append(deepcopy(courses))
si_students.append(deepcopy(students))
print "Running Trading Combinatorial Simulation..."
trading_cycle_matching(si_courses[9], si_students[9], combinatorial = True)
'''
# Percent of students matched with at least one course
def pct_students_one_course(to_compare):
	results = []
	for i in to_compare:
		results.append(float(sum([1 if len(s.assigned) > 0 else 0 for s in si_students[i]])) / float(nstudents))

	df = DataFrame.from_dict({'mechanism': sublist(mechanisms, to_compare), 'pct_students': results})
	results = map(lambda x: x * 100, results)
	return (results, bar_graph(df, "% Students Matched with >= 1 Course\n"))

# percent of students who receive first choice course
def pct_students_first_choice(to_compare):
	results = []
	for i in to_compare:
		results.append(float(sum([1 if len(s.assigned) > 0 and (s.preference[0] in s.assigned) else 0 for s in si_students[i]])) / float(nstudents))
	results = map(lambda x: x * 100, results)

	df = DataFrame.from_dict({'mechanism': sublist(mechanisms, to_compare), 'pct_students': results})
	return (results, bar_graph(df, "% Students Matched With Top Choice\n"))

# average rank of allotted courses
def avg_rank(to_compare):
	results = []
	for i in to_compare:
		sum_avg_rank = 0
		for s in si_students[i]:
			if len(s.assigned) > 0:
				sum_ranks = sum([s.preference.index(c) for c in s.assigned])
				avg_rank = float(sum_ranks) / len(s.assigned)
			else:
				avg_rank = s.threshold + 1
			sum_avg_rank += avg_rank
		
		results.append(float(sum_avg_rank) / len(students))

	df = DataFrame.from_dict({'mechanism': sublist(mechanisms, to_compare), 'pct_students': results})
	return (results, bar_graph(df, "Average Rank of Student's Courses\n"))

results, graph = pct_students_one_course(range(8))
print results
print graph

results, graph = pct_students_first_choice(range(8))
print results
print graph