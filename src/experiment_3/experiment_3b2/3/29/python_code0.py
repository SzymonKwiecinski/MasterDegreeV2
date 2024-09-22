import pulp
import json

# Input data
data_json = '{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

# Define the problem
problem = pulp.LpProblem("Minimize_D", pulp.LpMinimize)

# Decision Variables
a = pulp.LpVariable('a', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
D = pulp.LpVariable('D', cat='Continuous')
y = data['Y']
x = data['X']

# Objective
problem += D

# Constraints
for k in range(data['NumObs']):
    problem += (y[k] - (b * x[k] + a)) <= D
    problem += ((b * x[k] + a) - y[k]) <= D

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')