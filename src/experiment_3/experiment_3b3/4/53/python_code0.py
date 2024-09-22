import pulp

# Data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Create the problem
problem = pulp.LpProblem("SoybeanTransportation", pulp.LpMinimize)

# Decision Variables
x_vars = [
    [pulp.LpVariable(f"x_{i}_{j}", lowBound=0, cat='Continuous') for j in range(data['NumDestinations'])]
    for i in range(data['NumTerminals'])
]

# Objective Function
problem += pulp.lpSum(
    data['Cost'][i][j] * x_vars[i][j]
    for i in range(data['NumTerminals'])
    for j in range(data['NumDestinations'])
)

# Supply Constraints
for i in range(data['NumTerminals']):
    problem += (pulp.lpSum(x_vars[i][j] for j in range(data['NumDestinations'])) <= data['Supply'][i], f"Supply_Constraint_{i}")

# Demand Constraints
for j in range(data['NumDestinations']):
    problem += (pulp.lpSum(x_vars[i][j] for i in range(data['NumTerminals'])) == data['Demand'][j], f"Demand_Constraint_{j}")

# Solve the problem
problem.solve()

# Print the results
distribution = []
for i in range(data['NumTerminals']):
    for j in range(data['NumDestinations']):
        amount = pulp.value(x_vars[i][j])
        if amount > 0:
            distribution.append({
                'from': i,
                'to': j,
                'amount': amount
            })

total_cost = pulp.value(problem.objective)
output = {
    'distribution': distribution,
    'total_cost': total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')