import pulp

# Parsing the data
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

# Define the problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((k, l) for k in range(num_terminals) for l in range(num_destinations)),
                          lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(cost[k][l] * x[(k, l)] for k in range(num_terminals) for l in range(num_destinations))

# Supply constraints
for k in range(num_terminals):
    problem += pulp.lpSum(x[(k, l)] for l in range(num_destinations)) <= supply[k]

# Demand constraints
for l in range(num_destinations):
    problem += pulp.lpSum(x[(k, l)] for k in range(num_terminals)) == demand[l]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')