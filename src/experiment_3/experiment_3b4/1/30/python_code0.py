import pulp

# Extract data from JSON-like input
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Initialize the linear programming problem
problem = pulp.LpProblem("Quadratic_Regression", pulp.LpMinimize)

# Number of data points
K = len(data['x'])

# Decision Variables
c = pulp.LpVariable('c', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
a = pulp.LpVariable('a', cat='Continuous')
z = [pulp.LpVariable(f'z_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(z), "Minimize Sum of Absolute Deviation"

# Constraints
for k in range(K):
    x_k = data['x'][k]
    y_k = data['y'][k]
    
    # |y_k - (c*x_k^2 + b*x_k + a)| <= z_k
    problem += y_k - (c*x_k**2 + b*x_k + a) <= z[k]
    problem += (c*x_k**2 + b*x_k + a) - y_k <= z[k]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')