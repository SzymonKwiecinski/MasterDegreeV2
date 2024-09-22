import pulp

# Data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}
Y = data['Y']
X = data['X']
K = data['NumObs']

# Problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
z = pulp.LpVariable('z', lowBound=0, upBound=None, cat='Continuous')

# Objective
problem += z

# Constraints
for k in range(K):
    problem += (Y[k] - (b * X[k] + a) <= z)
    problem += ((b * X[k] + a) - Y[k] <= z)

# Solve
problem.solve()

# Results
intercept = a.varValue
slope = b.varValue

# Output
output = {"intercept": intercept, "slope": slope}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')