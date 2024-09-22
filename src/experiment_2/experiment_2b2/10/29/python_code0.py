import pulp

# Input data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Number of observations
K = data["NumObs"]
y = data["Y"]
x = data["X"]

# Define the problem
problem = pulp.LpProblem("Best_Fitting_Line", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('a')  # intercept
b = pulp.LpVariable('b')  # slope
d_max = pulp.LpVariable('d_max', lowBound=0)  # max deviation

# Objective function
problem += d_max, "Minimize_Maximum_Deviation"

# Constraints
for k in range(K):
    problem += y[k] - (a + b * x[k]) <= d_max, f"Deviation_Upper_{k}"
    problem += (a + b * x[k]) - y[k] <= d_max, f"Deviation_Lower_{k}"

# Solve the problem
problem.solve()

# Output
result = {
    "intercept": pulp.value(a),
    "slope": pulp.value(b)
}
print(result)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')