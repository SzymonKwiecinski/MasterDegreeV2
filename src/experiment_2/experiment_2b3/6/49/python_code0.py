import pulp

# Problem setup
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

P = len(prices)
M = len(machine_costs)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Objective function: Maximize total profit
total_profit = pulp.lpSum([
    batches[p] * prices[p] - 
    pulp.lpSum([time_required[m][p] * machine_costs[m] * batches[p] for m in range(M)]) 
    for p in range(P)
])

problem += total_profit

# Constraints
# Machine availability constraints
for m in range(M-1):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"availability_constraint_{m}"

# Combined availability for machine M and M-1
problem += pulp.lpSum([time_required[M-1][p] * batches[p] for p in range(P)]) <= availability[M-1], "combined_availability_M_M-1"

# Solve the problem
problem.solve()

# Extract results
batches_values = [pulp.value(batches[p]) for p in range(P)]
total_profit_value = pulp.value(problem.objective)

output = {
    "batches": batches_values,
    "total_profit": total_profit_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')