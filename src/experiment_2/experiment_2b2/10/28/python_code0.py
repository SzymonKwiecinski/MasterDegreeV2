import pulp

# Data Input
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = data['K']
Y = data['Y']
X = data['X']

# Problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('a', lowBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, cat='Continuous')
d = [pulp.LpVariable(f'd_{i}', lowBound=0, cat='Continuous') for i in range(K)]

# Objective Function
problem += pulp.lpSum(d)

# Constraints
for i in range(K):
    problem += Y[i] - (b * X[i] + a) <= d[i]
    problem += Y[i] - (b * X[i] + a) >= -d[i]

# Solve
problem.solve()

# Results
intercept = a.varValue
slope = b.varValue

# Print outputs in required format
output = {
    "intercept": intercept,
    "slope": slope
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')