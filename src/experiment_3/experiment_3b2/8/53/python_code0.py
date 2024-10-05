import pulp
import json

# Data input
data = json.loads('{"NumTerminals": 3, "NumDestinations": 4, "Cost": [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], "Demand": [65, 70, 50, 45], "Supply": [150, 100, 100]}')

# Extracting data
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Indices
A = [(i, j) for i in range(num_terminals) for j in range(num_destinations)]
k_indices = range(num_terminals)
l_indices = range(num_destinations)

# Problem Definition
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", A, lowBound=0)

# Objective Function
problem += pulp.lpSum(cost[i][j] * amount[(i, j)] for i in range(num_terminals) for j in range(num_destinations))

# Supply Constraints
for k in k_indices:
    problem += pulp.lpSum(amount[(k, j)] for j in range(num_destinations)) <= supply[k]

# Demand Constraints
for l in l_indices:
    problem += pulp.lpSum(amount[(i, l)] for i in range(num_terminals)) >= demand[l]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')