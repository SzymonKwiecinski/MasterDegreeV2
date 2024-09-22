import pulp

# Define the data
data = {
    "NumTerminals": 3,
    "NumDestinations": 4,
    "Cost": [[34, 49, 17, 26],
             [52, 64, 23, 14],
             [20, 28, 12, 17]],
    "Demand": [65, 70, 50, 45],
    "Supply": [150, 100, 100]
}

# Extracting parameters
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Initialize the problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Define decision variables
amounts = pulp.LpVariable.dicts("amount",
                                ((i, j) for i in range(num_terminals)
                                         for j in range(num_destinations)),
                                lowBound=0,
                                cat='Continuous')

# Define the objective function
problem += pulp.lpSum(cost[i][j] * amounts[i, j] for i in range(num_terminals) for j in range(num_destinations))

# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amounts[i, j] for j in range(num_destinations)) <= supply[i]

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amounts[i, j] for i in range(num_terminals)) >= demand[j]

# Solve the problem
problem.solve()

# Prepare output
total_cost = pulp.value(problem.objective)
distribution = [{"from": i, "to": j, "amount": amounts[i, j].varValue} for i in range(num_terminals) for j in range(num_destinations)]

output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')