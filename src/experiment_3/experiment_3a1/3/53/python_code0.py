import pulp
import json

# Given data in JSON format
data_json = '{"NumTerminals": 3, "NumDestinations": 4, "Cost": [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], "Demand": [65, 70, 50, 45], "Supply": [150, 100, 100]}'
data = json.loads(data_json)

# Extract data
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Define sets
K = range(num_terminals)  # Terminal cities
L = range(num_destinations)  # Destination cities
A = [(i, j) for i in K for j in L]  # All routes from terminals to destinations

# Define the problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", A, lowBound=0)

# Objective function
problem += pulp.lpSum(cost[i][j] * amount[(i, j)] for i in K for j in L), "Total_Cost"

# Supply constraints
for k in K:
    problem += pulp.lpSum(amount[(k, j)] for j in L) <= supply[k], f"Supply_Constraint_{k}"

# Demand constraints
for l in L:
    problem += pulp.lpSum(amount[(i, l)] for i in K) >= demand[l], f"Demand_Constraint_{l}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')