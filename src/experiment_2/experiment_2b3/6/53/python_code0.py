import pulp

# Data from JSON
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

# Problem definition
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Sets
terminals = range(data['NumTerminals'])
destinations = range(data['NumDestinations'])

# Decision Variables
amount = pulp.LpVariable.dicts("amount",
                               ((i, j) for i in terminals for j in destinations),
                               lowBound=0,
                               cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Cost'][i][j] * amount[i, j] for i in terminals for j in destinations)

# Constraints for Supply Limits
for i in terminals:
    problem += pulp.lpSum(amount[i, j] for j in destinations) <= data['Supply'][i], f"Supply_{i}"

# Constraints for Demand Fulfillment
for j in destinations:
    problem += pulp.lpSum(amount[i, j] for i in terminals) >= data['Demand'][j], f"Demand_{j}"

# Solve the problem
problem.solve()

# Extracting results
distribution = [
    {
        "from": i,
        "to": j,
        "amount": pulp.value(amount[i, j])
    }
    for i in terminals for j in destinations
]

output = {
    "distribution": distribution,
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')