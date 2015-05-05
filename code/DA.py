# deferred acceptance algorithm 
def deferred(courses, students, tiered = False, limit = 4, combinatorial = False, ndivisions = 8):
	changes = True 

	while changes == True: 
		changes = send_requests(courses, students, limit = limit, combinatorial = combinatorial, ndivisions = ndivisions)
		review_requests(courses, students, combinatorial = combinatorial, tiered = tiered, ndivisions = ndivisions) 

#students send requests to courses, s.t. if all requests accepted, they would each have filled courses up to limti 
def send_requests(courses, students, limit = 4, combinatorial = False, ndivisions = 8):	
	changes = False 
	for student in students: 
		space_left = limit - student.num_assigned 
		if not combinatorial:
			#send requests to the most preferred courses that haven't yet been requested 
			for i in range(space_left): 
				if student.next < student.threshold: 
					course_id = student.preference[student.next]
					send_request(courses, student, course_id)
					student.next += 1 
					changes = True 
		else:
			to_request = []
			request_groups = []
			counter = 0 
			#find most preferred courses not in currently possessed divisions to request 
			while ((len(to_request) < space_left) and (len(student.preference) > counter)):
				course_id = student.preference[counter]
				request_group = group(course_id, len(courses), ndivisions)
				if ((request_group not in student.groups_filled) and (request_group not in request_groups)):
					if course_id not in student.already_requested:
						to_request = to_request + [course_id]
						request_groups = request_groups + [request_group]
						student.already_requested = student.already_requested + [course_id]
				counter += 1 
			#send requests to all those courses 
			for course_id in to_request: 
				send_request(courses, student, course_id)
				changes = True 
	return changes 

#courses review requests and send acceptances and denials 
def review_requests(courses, students, combinatorial = False, tiered = False, ndivisions = 8):
	for course in courses: 
		for request in course.requests:
			#if course not full, accept 
			if course.num_assigned < course.cap:
				send_acceptance(courses, students, course, request, ndivisions, combinatorial)
				accept_request(course, request)
				course.num_assigned += 1 

			#if course full and boot criterion is met 
			#boot lowest preferred student in favor of requester
			elif willing_to_boot(course, request, tiered = tiered):
				send_acceptance(courses, students, course, request, ndivisions, combinatorial)
				send_rejection(courses, students, course, ndivisions, combinatorial)
				accept_request(course, request)

		#empty out requests
		course.requests = []


#returns group that course is in, where in combinatorial version, no student wants two courses from same group 
def group(course_id, ncourses, ndivisions):
	return course_id / (ncourses / ndivisions)

#determines whether course is willing to boot a student in favor of requesting student 
def willing_to_boot(course, request, tiered = False): 
	worst_rank = course.assigned[-1][0] 
	request_rank = request[0]
	if not tiered: 
		return (worst_rank > request_rank) 
	else:
		tier_size = len(course.preference) / 4 
		return ((worst_rank / tier_size) > (request_rank / tier_size))

#send a request from the given student to the course with the given ID 
def send_request(courses, student, course_id): 
	course_pref = (courses[course_id].preference).index(student.ID)
	courses[course_id].requests = courses[course_id].requests + [(course_pref, student.ID)]

#update roster of given course to include requester behind given request
def accept_request(course, request):
	course.assigned = course.assigned + [(request)]
	(course.assigned).sort()

#sends a tentative acceptance from given course to given requester 
def send_acceptance(courses, students, course, request, ndivisions, combinatorial):
	requester_id = request[1]
	requester = students[requester_id]
	requester.assigned = requester.assigned + [course.ID]
	requester.num_assigned += 1 
	if combinatorial:
		requester.groups_filled = requester.groups_filled + [group(course.ID, len(courses), ndivisions)]

#sends a rejection to a previously tentatively accepted requester, now booted in favor of new requester
def send_rejection(courses, students, course, ndivisions, combinatorial):
	deleted = (course.assigned).pop()
	rejected_id = deleted[1]
	rejected = students[rejected_id]
	(rejected.assigned).remove(course.ID)
	rejected.num_assigned -= 1 
	if combinatorial: 
		(rejected.groups_filled).remove(group(course.ID, len(courses), ndivisions))

