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

# Initialize the LP problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount",
                               [(i, j) for i in range(num_terminals) for j in range(num_destinations)],
                               lowBound=0,
                               cat='Continuous')

# Objective function
problem += pulp.lpSum(cost[i][j] * amount[(i, j)] for i in range(num_terminals) for j in range(num_destinations))

# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amount[(i, j)] for j in range(num_destinations)) <= supply[i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amount[(i, j)] for i in range(num_terminals)) >= demand[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Preparing output
distribution = [{"from": i, "to": j, "amount": pulp.value(amount[(i, j)])}
                for i in range(num_terminals) for j in range(num_destinations)]

output = {
    "distribution": distribution,
    "total_cost": pulp.value(problem.objective)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')