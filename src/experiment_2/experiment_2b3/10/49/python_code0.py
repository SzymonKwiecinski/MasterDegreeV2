import pulp

# Parse the input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

M = len(time_required)  # Number of machines
P = len(prices)         # Number of parts

# Create a LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables: number of batches to produce for each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Objective function: Maximize profit
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
cost = pulp.lpSum(machine_costs[m] * time_required[m][p] * batches[p] for p in range(P) for m in range(M))
problem += profit - cost, "Total_Profit"

# Constraints: Machine time availability
for m in range(M - 1):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_{m}_Availability"

# Combined constraint for Machine M and M-1 sharing availability
problem += pulp.lpSum(time_required[M-1][p] * batches[p] for p in range(P)) + pulp.lpSum(time_required[M-2][p] * batches[p] for p in range(P)) <= availability[M-1], "Shared_Availability"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')