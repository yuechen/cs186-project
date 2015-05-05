####################################################
# CS 186 Final Project: Course Matching
# Harvard University
# 
# Yuechen Zhao <yuechenzhao@college.harvard.edu>
# Last Modified: May 3, 2015
#
# Generates a distribution plot for the distribution
# used for generating course capacities.
#####################################################

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

samples = np.random.normal(20, 5, 85000).tolist() + np.random.normal(100, 30, 15000).tolist()
samples = filter(lambda x: x > 0, samples)

# the histogram of the data
n, bins, patches = plt.hist(samples, 200)
plt.xlabel("Course Capacity")
plt.ylabel("Number of Courses")
plt.show()