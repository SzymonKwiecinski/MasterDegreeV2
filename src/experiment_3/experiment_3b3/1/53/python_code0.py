import pulp

# Data from JSON
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Create the problem
problem = pulp.LpProblem("Soybean_Distribution", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", ((i, j) for i in range(data['NumTerminals']) 
                                          for j in range(data['NumDestinations'])), 
                               lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([data['Cost'][i][j] * amount[i, j] 
                       for i in range(data['NumTerminals']) 
                       for j in range(data['NumDestinations'])])

# Supply Constraints
for k in range(data['NumTerminals']):
    problem += pulp.lpSum([amount[k, j] for j in range(data['NumDestinations'])]) <= data['Supply'][k]

# Demand Constraints
for l in range(data['NumDestinations']):
    problem += pulp.lpSum([amount[i, l] for i in range(data['NumTerminals'])]) >= data['Demand'][l]

# Solve the problem
problem.solve()

# Output the results
distribution = [{'from': i, 'to': j, 'amount': pulp.value(amount[i, j])} 
                for i in range(data['NumTerminals']) 
                for j in range(data['NumDestinations'])]

total_cost = pulp.value(problem.objective)

output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')