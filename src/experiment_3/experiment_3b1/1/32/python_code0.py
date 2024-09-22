import pulp
import json

# Data provided in JSON format
data = json.loads('{"NumProducts": 2, "NumMachines": 2, "ProduceTime": [[1, 3], [2, 1]], "AvailableTime": [200, 100], "Profit": [20, 10]}')

# Defining the parameters
K = data['NumProducts']
S = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Create the problem variable
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision variables
q = pulp.LpVariable.dicts("q", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum([profit[k] * q[k] for k in range(K)]), "Total Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum([produce_time[k][s] * q[k] for k in range(K)]) <= available_time[s], f"TimeConstraint_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')