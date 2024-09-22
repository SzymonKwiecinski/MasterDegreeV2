import pulp

# Data from the JSON format
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

# Define the problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision variables: amount of soybeans shipped from terminal i to destination j
amount = pulp.LpVariable.dicts("Amount", ((i, j) for i in range(num_terminals) for j in range(num_destinations)), lowBound=0, cat='Continuous')

# Objective function: Minimize the total transportation cost
problem += pulp.lpSum(amount[i, j] * cost[i][j] for i in range(num_terminals) for j in range(num_destinations))

# Constraints
# Supply constraints: The total amount shipped from each terminal should not exceed its supply
for i in range(num_terminals):
    problem += pulp.lpSum(amount[i, j] for j in range(num_destinations)) <= supply[i]

# Demand constraints: The total amount received by each destination should meet its demand
for j in range(num_destinations):
    problem += pulp.lpSum(amount[i, j] for i in range(num_terminals)) >= demand[j]

# Solve the problem
problem.solve()

# Prepare the output
distribution = [
    {"from": i, "to": j, "amount": amount[i, j].varValue}
    for i in range(num_terminals) for j in range(num_destinations)
]

total_cost = pulp.value(problem.objective)

output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')