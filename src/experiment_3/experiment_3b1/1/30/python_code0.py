import pulp

# Data from JSON format
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Create the problem variable
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Variables for the coefficients of the quadratic function
c = pulp.LpVariable("c", lowBound=None)  # Coefficient of x^2
b = pulp.LpVariable("b", lowBound=None)  # Coefficient of x
a = pulp.LpVariable("a", lowBound=None)  # Constant term

# Number of data points
K = len(data['y'])

# Slack variables for deviations
d_plus = [pulp.LpVariable(f"d_plus_{k}", lowBound=0) for k in range(K)]
d_minus = [pulp.LpVariable(f"d_minus_{k}", lowBound=0) for k in range(K)]

# Objective function: Minimize the sum of deviations
problem += pulp.lpSum(d_plus[k] + d_minus[k] for k in range(K)), "Minimize_Absolute_Deviation"

# Constraints for each data point
for k in range(K):
    problem += d_plus[k] >= data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a), f"Pos_Dev_Constraint_{k}"
    problem += d_minus[k] >= -(data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a)), f"Neg_Dev_Constraint_{k}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')