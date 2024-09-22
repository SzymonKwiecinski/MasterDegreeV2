import pulp

# Data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", [(i, j) for i in range(num_terminals) for j in range(num_destinations)], lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(cost[i][j] * x[i, j] for i in range(num_terminals) for j in range(num_destinations))

# Constraints
# Supply constraints
for k in range(num_terminals):
    problem += pulp.lpSum(x[k, j] for j in range(num_destinations)) <= supply[k]

# Demand constraints
for l in range(num_destinations):
    problem += pulp.lpSum(x[i, l] for i in range(num_terminals)) >= demand[l]

# Solve the problem
problem.solve()

# Results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')