import pulp
import json

# Data input
data_json = '{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

# Create the LP problem
problem = pulp.LpProblem("LinearRegression", pulp.LpMinimize)

# Variables
b = pulp.LpVariable("slope", cat='Continuous')
a = pulp.LpVariable("intercept", cat='Continuous')
z = pulp.LpVariable("max_deviation", cat='Continuous')

# Constraints
for k in range(data['NumObs']):
    y_k = data['Y'][k]
    x_k = data['X'][k]
    
    # Deviation constraints
    problem += (y_k - (b * x_k + a) <= z)
    problem += (-(y_k - (b * x_k + a)) <= z)

# Objective function
problem += z

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the results
print(f'Intercept (a): {a.varValue}')
print(f'Slope (b): {b.varValue}')