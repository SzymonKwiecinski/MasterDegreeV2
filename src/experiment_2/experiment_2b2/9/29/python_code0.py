import pulp

# Define the data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extract X and Y values
Y = data['Y']
X = data['X']
K = data['NumObs']

# Define the problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

# Define the variables
a = pulp.LpVariable('a', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
d = pulp.LpVariable('d', lowBound=0)

# Objective function:
problem += d, "Objective is to minimize the maximum deviation"

# Constraints:
for k in range(K):
    problem += (Y[k] - (b * X[k] + a) <= d), f"Constraint_upper_{k}"
    problem += (-(Y[k] - (b * X[k] + a)) <= d), f"Constraint_lower_{k}"

# Solve the problem
problem.solve()

# Output the results
result = {
    "intercept": pulp.value(a),
    "slope": pulp.value(b)
}

print(result)

print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")