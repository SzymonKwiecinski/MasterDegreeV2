import pulp

# Define the problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']

# Indices for routes
routes = [(i, j) for i in range(num_terminals) for j in range(num_destinations)]

# Decision Variables
amount = pulp.LpVariable.dicts("amount", routes, lowBound=0, cat=pulp.LpContinuous)

# Objective Function
problem += pulp.lpSum(cost[i][j] * amount[(i, j)] for i, j in routes)

# Supply Constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amount[(i, j)] for j in range(num_destinations)) <= supply[i]

# Demand Constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amount[(i, j)] for i in range(num_terminals)) >= demand[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')