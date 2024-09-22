import pulp

# Input data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = data['NumObs']
y = data['Y']
x = data['X']

# Create the problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('a', lowBound=None, upBound=None)
b = pulp.LpVariable('b', lowBound=None, upBound=None)
d = pulp.LpVariable('d', lowBound=0)

# Objective function: Minimize the maximum deviation (d)
problem += d

# Constraints
for k in range(K):
    problem += y[k] - (b * x[k] + a) <= d
    problem += (b * x[k] + a) - y[k] <= d

# Solve the problem
problem.solve()

# Retrieve results
intercept = pulp.value(a)
slope = pulp.value(b)

output = {
    "intercept": intercept,
    "slope": slope
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')