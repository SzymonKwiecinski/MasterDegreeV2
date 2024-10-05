import pulp

# Data from JSON
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Initialize the problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Indices for terminals and destinations
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']

# Decision variables
amount = pulp.LpVariable.dicts("amount",
                               ((i, j) for i in range(num_terminals) for j in range(num_destinations)),
                               lowBound=0,
                               cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Cost'][i][j] * amount[(i, j)] for i in range(num_terminals) for j in range(num_destinations))

# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amount[(i, j)] for j in range(num_destinations)) <= data['Supply'][i]

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amount[(i, j)] for i in range(num_terminals)) >= data['Demand'][j]

# Solve the problem
problem.solve()

# Output the results
distribution = [{'from': i, 'to': j, 'amount': amount[(i, j)].varValue}
                for i in range(num_terminals) for j in range(num_destinations)]
total_cost = pulp.value(problem.objective)

print(f'Distribution: {distribution}')
print(f'Total Cost (Objective Value): <OBJ>{total_cost}</OBJ>')