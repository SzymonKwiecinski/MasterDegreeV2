import pulp

# Define the data
num_terminals = 3
num_destinations = 4
cost = [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]]
demand = [65, 70, 50, 45]
supply = [150, 100, 100]

# Initialize the problem
problem = pulp.LpProblem("Soybean_Transport_Problem", pulp.LpMinimize)

# Decision variables
amounts = [
    [pulp.LpVariable(f'amount_{i}_{j}', lowBound=0, cat='Continuous') for j in range(num_destinations)]
    for i in range(num_terminals)
]

# Objective function
problem += pulp.lpSum(cost[i][j] * amounts[i][j] for i in range(num_terminals) for j in range(num_destinations))

# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amounts[i][j] for j in range(num_destinations)) <= supply[i]

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amounts[i][j] for i in range(num_terminals)) >= demand[j]

# Solve the problem
problem.solve()

# Prepare the output
distribution = [
    {"from": i, "to": j, "amount": pulp.value(amounts[i][j])}
    for i in range(num_terminals) for j in range(num_destinations)
]

total_cost = pulp.value(problem.objective)

# Display the results
output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')