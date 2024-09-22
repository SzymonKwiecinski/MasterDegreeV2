import pulp

# Data input
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

# Problem
problem = pulp.LpProblem("SoybeanTransportation", pulp.LpMinimize)

# Decision variables
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
x = pulp.LpVariable.dicts("shipment",
                          ((i, j) for i in range(num_terminals) for j in range(num_destinations)),
                          lowBound=0,
                          cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Cost'][i][j] * x[(i, j)] for i in range(num_terminals) for j in range(num_destinations))

# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(x[(i, j)] for j in range(num_destinations)) <= data['Supply'][i]

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(x[(i, j)] for i in range(num_terminals)) >= data['Demand'][j]

# Solve
problem.solve()

# Output
distribution = [
    {"from": i, "to": j, "amount": pulp.value(x[i, j])}
    for i in range(num_terminals)
    for j in range(num_destinations)
]

total_cost = pulp.value(problem.objective)

output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')