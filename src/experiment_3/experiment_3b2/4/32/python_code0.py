import pulp
import json

# Data in JSON format
data = '{"NumProducts": 2, "NumMachines": 2, "ProduceTime": [[1, 3], [2, 1]], "AvailableTime": [200, 100], "Profit": [20, 10]}'
parameters = json.loads(data)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(parameters['NumProducts']), lowBound=0)

# Objective function
problem += pulp.lpSum(parameters['Profit'][k] * x[k] for k in range(parameters['NumProducts']))

# Constraints
for s in range(parameters['NumMachines']):
    problem += pulp.lpSum(parameters['ProduceTime'][k][s] * x[k] for k in range(parameters['NumProducts'])) <= parameters['AvailableTime'][s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')