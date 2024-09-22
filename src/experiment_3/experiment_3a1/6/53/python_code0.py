import pulp

# Data from JSON
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Define problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Variables
amount = pulp.LpVariable.dicts("amount", (range(data['NumTerminals']), range(data['NumDestinations'])), lowBound=0)

# Objective function
problem += pulp.lpSum(data['Cost'][i][j] * amount[i][j] for i in range(data['NumTerminals']) for j in range(data['NumDestinations']))

# Supply constraints
for k in range(data['NumTerminals']):
    problem += pulp.lpSum(amount[k][j] for j in range(data['NumDestinations'])) <= data['Supply'][k]

# Demand constraints
for l in range(data['NumDestinations']):
    problem += pulp.lpSum(amount[i][l] for i in range(data['NumTerminals'])) >= data['Demand'][l]

# Solve the problem
problem.solve()

# Output results
distribution = [{"from": i, "to": j, "amount": pulp.value(amount[i][j])} for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])]

total_cost = pulp.value(problem.objective)

print(f'Distribution: {distribution}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')