import pulp

# Data from the provided JSON
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Indices
terminals = range(data['NumTerminals'])
destinations = range(data['NumDestinations'])

# Create the problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("Amount",
                               ((i, j) for i in terminals for j in destinations),
                               lowBound=0,
                               cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Cost'][i][j] * amount[i, j] for i in terminals for j in destinations)

# Supply constraints
for k in terminals:
    problem += pulp.lpSum(amount[k, j] for j in destinations) <= data['Supply'][k]

# Demand constraints
for l in destinations:
    problem += pulp.lpSum(amount[i, l] for i in terminals) >= data['Demand'][l]

# Solve the problem
problem.solve()

# Output results
distribution = {(i, j): amount[i, j].varValue for i in terminals for j in destinations if amount[i, j].varValue > 0}

print("Distribution (i, j, amount):")
for (i, j), amt in distribution.items():
    print(f"Route ({i}, {j}): {amt} tons")

print(f"Total transportation cost (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")