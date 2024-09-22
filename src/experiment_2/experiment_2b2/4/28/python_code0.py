import pulp
import json

# Load data from JSON format
data = json.loads('{"K": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

# Extract data
K = data['K']
Y = data['Y']
X = data['X']

# Initialize the linear optimization problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('a', lowBound=None, cat='Continuous')  # Intercept
b = pulp.LpVariable('b', lowBound=None, cat='Continuous')  # Slope
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(K)]  # Absolute deviations

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(d), "Minimize_Sum_of_Absolute_Deviations"

# Constraints: d_k >= y_k - (a + b*x_k) and d_k >= -(y_k - (a + b*x_k))
for k in range(K):
    problem += Y[k] - (a + b * X[k]) <= d[k], f"Deviation_Above_{k}"
    problem += -(Y[k] - (a + b * X[k])) <= d[k], f"Deviation_Below_{k}"

# Solve the problem
problem.solve()

# Output results
solution = {
    "intercept": pulp.value(a),
    "slope": pulp.value(b)
}

# Print solution
print(json.dumps(solution, indent=2))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')