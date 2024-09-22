import pulp
import json

# Data in JSON format
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 
                       1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 
              5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = data['K']
Y = data['Y']
X = data['X']

# Create the problem
problem = pulp.LpProblem("LineFitting", pulp.LpMinimize)

# Variables
b = pulp.LpVariable('b', None)  # Slope
a = pulp.LpVariable('a', None)  # Intercept
d = [pulp.LpVariable(f'd_{k}', lowBound=0) for k in range(K)]  # Deviation variables

# Objective function
problem += pulp.lpSum(d[k] for k in range(K)), "Minimize_Deviation"

# Constraints
for k in range(K):
    problem += d[k] >= Y[k] - (b * X[k] + a), f"Upper_Bound_Deviation_{k}"
    problem += d[k] >= -(Y[k] - (b * X[k] + a)), f"Lower_Bound_Deviation_{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')