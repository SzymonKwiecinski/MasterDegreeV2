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

num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
costs = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Creating the LP problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts(
    "amount",
    ((i, j) for i in range(num_terminals) for j in range(num_destinations)),
    lowBound=0,
    cat='Continuous'
)

# Objective Function
problem += pulp.lpSum(
    costs[i][j] * amount[i, j]
    for i in range(num_terminals)
    for j in range(num_destinations)
)

# Supply Constraints
for k in range(num_terminals):
    problem += pulp.lpSum(amount[k, j] for j in range(num_destinations)) <= supply[k]

# Demand Constraints
for l in range(num_destinations):
    problem += pulp.lpSum(amount[i, l] for i in range(num_terminals)) >= demand[l]

# Solve the problem
problem.solve()

# Output
distribution = [
    {"from": i, "to": j, "amount": pulp.value(amount[i, j])}
    for i in range(num_terminals)
    for j in range(num_destinations)
]

output = {
    "distribution": distribution,
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')