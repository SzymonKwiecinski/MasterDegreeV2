import pulp

# Provided data
data = {
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "min_batches": [10, 10, 10, 10]
}

# Unpacking data
time_required = data["time_required"]
machine_costs = data["machine_costs"]
availability = data["availability"]
prices = data["prices"]
min_batches = data["min_batches"]

# Indices
M = len(time_required)
P = len(prices)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Objective function: Maximize profit
profit = pulp.lpSum([batches[p] * prices[p] for p in range(P)]) - pulp.lpSum([
    machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)
])
problem += profit

# Constraints
# Machine 1 and 2 can share availability
problem += pulp.lpSum([
    pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M - 1)
]) <= sum(availability[:-1])

# Individual machine availability for the last machine
problem += pulp.lpSum([time_required[M-1][p] * batches[p] for p in range(P)]) <= availability[M-1]

# Solve the problem
problem.solve()

# Extract and print results
batches_produced = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')