import pulp
import json

# Data from JSON
data = json.loads('{"NumProducts": 2, "NumMachines": 2, "ProduceTime": [[1, 3], [2, 1]], "AvailableTime": [200, 100], "Profit": [20, 10]}')

# Extract data
K = data['NumProducts']
S = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profits = data['Profit']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(profits[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * x[k] for k in range(K)) <= available_time[s], f"Time_Constraint_{s + 1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')