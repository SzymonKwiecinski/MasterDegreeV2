import pulp
import json

# Given data
data = {
    'K': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Parameters for the linear model
intercept = 2.0  # Example intercept, set to the desired value
slope = 0.5      # Example slope, set to the desired value

# Create the LP problem
problem = pulp.LpProblem("Minimize_Absolute_Deviation", pulp.LpMinimize)

# Decision variables
z = pulp.LpVariable.dicts("z", range(data['K']), lowBound=0)

# Objective Function
problem += pulp.lpSum(z[k] for k in range(data['K'])), "Objective"

# Constraints
for k in range(data['K']):
    y_k = data['Y'][k]
    x_k = data['X'][k]
    problem += z[k] >= y_k - (slope * x_k + intercept), f"Constraint_1_{k}"
    problem += z[k] >= -(y_k - (slope * x_k + intercept)), f"Constraint_2_{k}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')