import pulp

# Parse input data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [
        [34, 49, 17, 26],
        [52, 64, 23, 14],
        [20, 28, 12, 17]
    ],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Number of terminals and destinations
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']

# Create a linear programming problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Create decision variables
routes = []
for i in range(num_terminals):
    row = []
    for j in range(num_destinations):
        var = pulp.LpVariable(f'x_{i}_{j}', lowBound=0, cat='Continuous')
        row.append(var)
    routes.append(row)

# Objective function
problem += pulp.lpSum(data['Cost'][i][j] * routes[i][j] 
                      for i in range(num_terminals) 
                      for j in range(num_destinations))

# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(routes[i][j] for j in range(num_destinations)) <= data['Supply'][i]

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(routes[i][j] for i in range(num_terminals)) >= data['Demand'][j]

# Solve the problem
problem.solve()

# Prepare output
distribution = [{"from": i, "to": j, "amount": pulp.value(routes[i][j])}
                for i in range(num_terminals)
                for j in range(num_destinations)]

output = {
    "distribution": distribution,
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')