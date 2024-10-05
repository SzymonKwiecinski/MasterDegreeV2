import pulp

# Read the input data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Extract the data
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Create the LP problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Create decision variables
amount = pulp.LpVariable.dicts(
    "amount",
    ((i, j) for i in range(num_terminals) for j in range(num_destinations)),
    lowBound=0,
    cat='Continuous'
)

# Objective function
problem += pulp.lpSum(cost[i][j] * amount[i, j] for i in range(num_terminals) for j in range(num_destinations))

# Constraints for supply
for i in range(num_terminals):
    problem += pulp.lpSum(amount[i, j] for j in range(num_destinations)) <= supply[i]

# Constraints for demand
for j in range(num_destinations):
    problem += pulp.lpSum(amount[i, j] for i in range(num_terminals)) >= demand[j]

# Solve the problem
problem.solve()

# Output the results
distribution = [{"from": i, "to": j, "amount": amount[i, j].varValue}
                for i in range(num_terminals) 
                for j in range(num_destinations)]

total_cost = pulp.value(problem.objective)

result = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')