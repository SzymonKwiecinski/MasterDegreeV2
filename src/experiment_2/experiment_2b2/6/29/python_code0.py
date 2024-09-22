import pulp

# Data from input
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Number of observations
K = data['NumObs']
Y = data['Y']
X = data['X']

# Create the problem
problem = pulp.LpProblem("Minimize_Maximum_Deviation", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('a', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
t = pulp.LpVariable('t', lowBound=0)  # This will be the maximum deviation

# Objective function: minimize maximum deviation
problem += t

# Constraints
for k in range(K):
    # Y[k] - (a + b * X[k]) <= t
    # (a + b * X[k]) - Y[k] <= t
    problem += Y[k] - (a + b * X[k]) <= t
    problem += (a + b * X[k]) - Y[k] <= t

# Solve the problem
problem.solve()

# Results
intercept = pulp.value(a)
slope = pulp.value(b)

# Output in required format
output = {
    "intercept": intercept,
    "slope": slope
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')