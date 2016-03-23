from pulp import *
import dataset_to_matrix as d2m


##########################################################################

def main():

	# PREPROCRESS DATA
	coursesFilename = ""
	timetableFilename = ""
	classroomFilename = ""

	capVector = d2m.capacityVector(classroomFilename)
	schedulingMatrix = d2m.schedulingMatrix(coursesFilename, timetableFilename)
	periodsCountVector = d2m.periodsCountVector(coursesFilename, timetableFilename)
	assignmentAvailMatrix = d2m.assignmentAvailabilityMatrix(coursesFilename, classroomFilename)

	t = len(schedulingMatrix)
	m = len(periodsCountVector)
	n = len(capVector)

	# ECHO PARAMETERS
	"""print "Scheduling Matrix:"
	for item in schedulingMatrix:
		print item
	print "periods Count Vector:"
	print periodsCountVector
	print "Assignment Availability Matrix:"
	for item in assignmentAvailMatrix:
		print item"""

	print "(t, m, n) = " + str((t, m, n))

	# INSTANTIATE DECISION VARIABLES
	x = LpVariable.dicts("assignment.binary.values", (range(t), range(m), range(n)), 0, 1, LpInteger)

	# INSTANTIATE A PROBLEM
	prob = LpProblem("cu.eng.classroom.assignment.problem", LpMinimize)

	# DEFINE OBJECTIVE FUNCTION
	prob += lpSum([capVector[j]*x[p][i][j] for p in range(t) for i in range(m) for j in range(n)])

	# DEFINE CONSTRAINTS
	for p in range(t):
		for i in range(m):
			prob += lpSum([x[p][i][j] for j in range(n)]) == schedulingMatrix[p][i]#, "scheduling.constraint."+str(i)+"."+str(p)
			#print ""

	for p in range(t):
		for j in range(n):
			prob += lpSum([x[p][i][j] for i in range(m)]) <= 1#, "one.to.one.constraint."+str(j)+"."+str(p)

	for i in range(m):
		for j in range(n):
			prob += lpSum([x[p][i][j] for p in range(t)]) <= periodsCountVector[i]#, "periods.count.constraint."+str(i)+"."+str(j)

	for p in range(t):
		for i in range(m):
			for j in range(n):
				prob += x[p][i][j] <= assignmentAvailMatrix[i][j]#, "assignment.avail.constraint."+str(i)+"."+str(j)+"."+str(p)
	
	# SOLVE PROBLEM BY GLPK SOLVER
	GLPK().solve(prob)

	# PRINT OUTPUTS
	for v in prob.variables():
		print v.name + " = " + str(v.varValue)

	print "Objective value: " + str(value(prob.objective))


##########################################################################

if __name__ == "__main__":
	main()