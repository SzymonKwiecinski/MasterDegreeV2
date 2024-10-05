import pulp

# Data
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

# Define the problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("shipment", 
                          ((i, j) for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])), 
                          lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Cost'][i][j] * x[(i, j)] for i in range(data['NumTerminals']) for j in range(data['NumDestinations']))

# Constraints
# Supply Constraints
for i in range(data['NumTerminals']):
    problem += pulp.lpSum(x[(i, j)] for j in range(data['NumDestinations'])) <= data['Supply'][i]

# Demand Constraints
for j in range(data['NumDestinations']):
    problem += pulp.lpSum(x[(i, j)] for i in range(data['NumTerminals'])) >= data['Demand'][j]

# Solve the problem
problem.solve()

# Output
distribution = [
    {
        "from": i,
        "to": j,
        "amount": pulp.value(x[(i, j)])
    }
    for i in range(data['NumTerminals']) 
    for j in range(data['NumDestinations']) 
    if pulp.value(x[(i, j)]) > 0
]

output = {
    "distribution": distribution,
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')