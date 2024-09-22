import pulp

# Data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Indices
terminals = list(range(data['NumTerminals']))
destinations = list(range(data['NumDestinations']))
routes = [(i, j) for i in terminals for j in destinations]

# Decision variables
amount = pulp.LpVariable.dicts("amount", (terminals, destinations), lowBound=0, cat='Continuous')

# Problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Objective function
problem += pulp.lpSum(data['Cost'][i][j] * amount[i][j] for (i, j) in routes)

# Supply constraints
for i in terminals:
    problem += pulp.lpSum(amount[i][j] for j in destinations) <= data['Supply'][i]

# Demand constraints
for j in destinations:
    problem += pulp.lpSum(amount[i][j] for i in terminals) >= data['Demand'][j]

# Solve
problem.solve()

# Output
distribution = {(i, j): pulp.value(amount[i][j]) for i, j in routes if pulp.value(amount[i][j]) > 0}
print("Distribution of soybeans:")
for (i, j), value in distribution.items():
    print(f"From Terminal {i} to Destination {j}: {value} tons")

print(f"Total Transportation Cost (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")