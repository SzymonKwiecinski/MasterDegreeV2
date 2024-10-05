import pulp

# Data extracted from the given JSON format
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Number of observations
K = data['NumObs']
Y = data['Y']
X = data['X']

# Define the linear programming problem
problem = pulp.LpProblem("Minimize_Maximum_Deviation", pulp.LpMinimize)

# Decision Variables
a = pulp.LpVariable('Intercept', lowBound=None, upBound=None)
b = pulp.LpVariable('Slope', lowBound=None, upBound=None)
d = pulp.LpVariable('Maximum_Deviation', lowBound=0)

# Objective Function: Minimize Maximum Deviation
problem += d, "Objective: Minimize Maximum Deviation"

# Constraints to ensure deviation is calculated correctly
for k in range(K):
    problem += Y[k] - (a + b * X[k]) <= d, f"DeviationUpperBound_{k}"
    problem += (a + b * X[k]) - Y[k] <= d, f"DeviationLowerBound_{k}"

# Solve the problem
problem.solve()

# Output the results
intercept = pulp.value(a)
slope = pulp.value(b)

output = {
    "intercept": intercept,
    "slope": slope
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')