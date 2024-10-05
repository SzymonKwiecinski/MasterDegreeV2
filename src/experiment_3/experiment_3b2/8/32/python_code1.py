import pulp
import json

# Data extraction from JSON format
data = json.loads('{"NumProducts": 2, "NumMachines": 2, "ProduceTime": [[1, 3], [2, 1]], "AvailableTime": [200, 100], "Profit": [20, 10]}')

# Number of products and machines
K = data['NumProducts']
S = data['NumMachines']

# Create the linear programming problem
problem = pulp.LpProblem("Product_Optimization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
profit = data['Profit']
problem += pulp.lpSum([profit[k] * x[k] for k in range(K)])

# Constraints
produce_time = data['ProduceTime']
available_time = data['AvailableTime']

for s in range(S):
    problem += pulp.lpSum([produce_time[k][s] * x[k] for k in range(K)]) <= available_time[s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')