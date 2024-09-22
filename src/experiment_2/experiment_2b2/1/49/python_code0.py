import pulp

# Data provided in the JSON format
data = {
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10]
}

# Extract data
time_required = data["time_required"]
machine_costs = data["machine_costs"]
availability = data["availability"]
prices = data["prices"]
min_batches = data["min_batches"]

# Number of machines and parts
M = len(time_required)
P = len(time_required[0])

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches to produce for each part
batches = [pulp.LpVariable(f"batches_{p}", lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective function: Maximize total profit
revenue = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
costs = pulp.lpSum([machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M)])
profit = revenue - costs
problem += profit

# Constraints
# Machine time availability constraints
for m in range(M - 2):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Combined availability constraint for the last two machines
problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P) for m in [M-2, M-1]) <= availability[M-1]

# Solve the problem
problem.solve()

# Output the results
result = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')