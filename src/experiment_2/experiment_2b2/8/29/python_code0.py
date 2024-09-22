from pulp import LpProblem, LpVariable, lpSum, LpMinimize, value

# Data Input
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}
Y = data['Y']
X = data['X']
K = data['NumObs']

# Problem
problem = LpProblem("Minimize_Maximum_Deviation", LpMinimize)

# Variables
a = LpVariable('a', lowBound=-float('inf'), upBound=float('inf'))
b = LpVariable('b', lowBound=-float('inf'), upBound=float('inf'))
d = LpVariable('d', lowBound=0)

# Constraints
for k in range(K):
    problem += (Y[k] - (b * X[k] + a) <= d, f"Above_{k}")
    problem += ((b * X[k] + a) - Y[k] <= d, f"Below_{k}")

# Objective
problem += d

# Solve
problem.solve()

# Output
output = {"intercept": value(a), "slope": value(b)}
print(output)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')