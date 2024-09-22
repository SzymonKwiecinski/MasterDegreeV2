import pulp

# Define the data from the JSON
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Indices for terminals and destinations
terminals = range(data['NumTerminals'])
destinations = range(data['NumDestinations'])

# Create the LP problem
problem = pulp.LpProblem('Soybean_Transportation', pulp.LpMinimize)

# Create decision variables
amount = pulp.LpVariable.dicts("Amount",
                               ((i, j) for i in terminals for j in destinations),
                               lowBound=0,
                               cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Cost'][i][j] * amount[i, j] for i in terminals for j in destinations)

# Supply constraints
for i in terminals:
    problem += pulp.lpSum(amount[i, j] for j in destinations) <= data['Supply'][i], f"Supply_Constraint_{i}"

# Demand constraints
for j in destinations:
    problem += pulp.lpSum(amount[i, j] for i in terminals) >= data['Demand'][j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "distribution": [
        {"from": i, "to": j, "amount": pulp.value(amount[i, j])}
        for i in terminals for j in destinations
    ],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')