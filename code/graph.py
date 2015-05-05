from ggplot import *
from pandas import DataFrame

mechanisms = ["RDS", "RDS (C)", "HBS", "HBS (C)", "DA (U)", "DA (U, C)", "DA (T)", "DA (T, C)", "Trade", "Trade (C)"]

def sublist(l, indicies):
	return [l[i] for i in indicies]

def bar_graph(df, title):
	return ggplot(df, aes(x = 'mechanism', y = 'pct_students')) + \
	geom_bar(stat = 'identity') + theme_bw() + theme(axis_text_x  = element_text(size = 10)) + \
	ggtitle(title) + xlab("\nMechanism") + ylab("% of Students\n")

results = [74.53333333333333, 77.2, 97.46666666666667, 97.33333333333334, 87.53333333333333, 89.46666666666667, 88.26666666666667, 89.60000000000001]
df = DataFrame.from_dict({'mechanism': sublist(mechanisms, range(8)), 'pct_students': results})
print bar_graph(df, "% of Students With At Least One Course\n")