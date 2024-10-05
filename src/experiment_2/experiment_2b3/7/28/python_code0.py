import pulp

# Data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = data['K']
Y = data['Y']
X = data['X']

# Problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective
problem += pulp.lpSum(d), "Minimize_Sum_Absolute_Deviation"

# Constraints
for k in range(K):
    problem += Y[k] - (a + b * X[k]) <= d[k]
    problem += (a + b * X[k]) - Y[k] <= d[k]

# Solve
problem.solve()

# Output
intercept = a.varValue
slope = b.varValue

output = {
    "intercept": intercept,
    "slope": slope
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')