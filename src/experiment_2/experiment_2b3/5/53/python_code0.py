import pulp

# Given data
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

# Problem setup
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Variables: quantity shipped from terminal i to destination j
# x[i][j] represents the amount shipped from terminal i to destination j
x = [[pulp.LpVariable(f'x_{i}_{j}', lowBound=0, cat='Continuous') for j in range(data['NumDestinations'])] for i in range(data['NumTerminals'])]

# Objective function: Minimize the total transportation cost
problem += pulp.lpSum(data['Cost'][i][j] * x[i][j] for i in range(data['NumTerminals']) for j in range(data['NumDestinations']))

# Supply constraints: The total amount shipped from each terminal should not exceed its supply
for i in range(data['NumTerminals']):
    problem += pulp.lpSum(x[i][j] for j in range(data['NumDestinations'])) <= data['Supply'][i]

# Demand constraints: Demand at each destination must be met
for j in range(data['NumDestinations']):
    problem += pulp.lpSum(x[i][j] for i in range(data['NumTerminals'])) >= data['Demand'][j]

# Solve the problem
problem.solve()

# Output the results
distribution = [{'from': i, 'to': j, 'amount': pulp.value(x[i][j])} for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])]
total_cost = pulp.value(problem.objective)

# Output format
output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')