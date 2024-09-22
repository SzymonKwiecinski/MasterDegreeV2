import pulp

# Parse the input data
data = {'NumTerminals': 3, 'NumDestinations': 4, 'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 'Demand': [65, 70, 50, 45], 'Supply': [150, 100, 100]}

# Extract data
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
costs = data['Cost']
demands = data['Demand']
supplies = data['Supply']

# Create the LP problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables: amount of soybeans shipped from terminal i to destination j
amount = pulp.LpVariable.dicts("Amount", ((i, j) for i in range(num_terminals) for j in range(num_destinations)), lowBound=0, cat='Continuous')

# Objective function: Minimize the total transportation cost
problem += pulp.lpSum(costs[i][j] * amount[i, j] for i in range(num_terminals) for j in range(num_destinations))

# Constraints to satisfy supply at each terminal
for i in range(num_terminals):
    problem += pulp.lpSum(amount[i, j] for j in range(num_destinations)) <= supplies[i], f"Supply_Constraint_Terminal_{i}"

# Constraints to satisfy demand at each destination
for j in range(num_destinations):
    problem += pulp.lpSum(amount[i, j] for i in range(num_terminals)) >= demands[j], f"Demand_Constraint_Destination_{j}"

# Solve the problem
problem.solve()

# Prepare the output
distribution = [{"from": i, "to": j, "amount": amount[i, j].varValue} for i in range(num_terminals) for j in range(num_destinations)]
total_cost = pulp.value(problem.objective)

# Print results
output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')