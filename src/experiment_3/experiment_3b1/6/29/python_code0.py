import pulp
import json

# Given data in JSON format
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Create the problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

# Variables
M = pulp.LpVariable("M", lowBound=0)  # M >= 0
a = pulp.LpVariable("a")  # unrestricted
b = pulp.LpVariable("b")  # unrestricted

# Constraints and objective
for k in range(data['NumObs']):
    y_k = data['Y'][k]
    x_k = data['X'][k]
    
    problem += (y_k - (b * x_k + a) <= M, f"Constraint_Upper_{k}")
    problem += (-(y_k - (b * x_k + a)) <= M, f"Constraint_Lower_{k}")

# Objective function
problem += M, "Objective"

# Solve the problem
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Intercept (a): {pulp.value(a)}')
print(f'Slope (b): {pulp.value(b)}')