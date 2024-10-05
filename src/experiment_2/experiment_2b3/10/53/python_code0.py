import pulp

data = {'NumTerminals': 3, 'NumDestinations': 4, 'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 'Demand': [65, 70, 50, 45], 'Supply': [150, 100, 100]}

# Unpacking data
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
total_supply = data['Supply']
total_demand = data['Demand']

# Create the LP problem
problem = pulp.LpProblem("TransportationProblem", pulp.LpMinimize)

# Create decision variables for each route
route_variables = {}
for i in range(num_terminals):
    for j in range(num_destinations):
        route_variables[(i, j)] = pulp.LpVariable(f"x_{i}_{j}", 0, cat='Continuous')

# Objective function
problem += pulp.lpSum([route_variables[(i, j)] * cost[i][j] for i in range(num_terminals) for j in range(num_destinations)])

# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum([route_variables[(i, j)] for j in range(num_destinations)]) <= total_supply[i]

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum([route_variables[(i, j)] for i in range(num_terminals)]) >= total_demand[j]

# Solve the problem
problem.solve()

# Prepare the output
distribution = [{'from': i, 'to': j, 'amount': route_variables[(i, j)].varValue} for i in range(num_terminals) for j in range(num_destinations)]
total_cost = pulp.value(problem.objective)

output = {
    "distribution": distribution,
    "total_cost": total_cost
}

# Print the output
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')