import pulp

# Parse the data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Create the problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables
amount = [[pulp.LpVariable(f'amount_{i}_{j}', lowBound=0, cat='Continuous') for j in range(num_destinations)] for i in range(num_terminals)]

# Objective Function
problem += pulp.lpSum(cost[i][j] * amount[i][j] for i in range(num_terminals) for j in range(num_destinations))

# Supply Constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amount[i][j] for j in range(num_destinations)) <= supply[i]

# Demand Constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amount[i][j] for i in range(num_terminals)) >= demand[j]

# Solve the problem
problem.solve()

# Collect the results
distribution = []
for i in range(num_terminals):
    for j in range(num_destinations):
        distribution.append({
            "from": i,
            "to": j,
            "amount": amount[i][j].varValue
        })

total_cost = pulp.value(problem.objective)

# Output the result
output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')