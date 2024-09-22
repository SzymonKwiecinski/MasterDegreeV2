import pulp

# Data provided
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}
y = data["Y"]
x = data["X"]
K = data["K"]

# Problem
problem = pulp.LpProblem("Minimize Deviation", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('a')
b = pulp.LpVariable('b')
deviations = [pulp.LpVariable(f'd_{k}', lowBound=0) for k in range(K)]

# Objective function: minimize the sum of absolute deviations
problem += pulp.lpSum(deviations)

# Constraints
for k in range(K):
    problem += deviations[k] >= y[k] - (a + b * x[k])
    problem += deviations[k] >= -(y[k] - (a + b * x[k]))

# Solve the problem
problem.solve()

# Output
intercept = pulp.value(a)
slope = pulp.value(b)
result = {
    "intercept": intercept,
    "slope": slope
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')