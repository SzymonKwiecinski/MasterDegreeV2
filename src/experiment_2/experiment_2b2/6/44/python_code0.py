import pulp

# Data provided in JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extract data from the JSON structure
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of machines (M) and parts (P)
M = len(machine_costs)
P = len(prices)

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Create decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Objective Function: Maximize total profit
profit = pulp.lpSum([
    (prices[p] * batches[p]) - pulp.lpSum([time_required[m][p] * machine_costs[m] * batches[p] for m in range(M)])
    for p in range(P)
])
problem += profit

# Constraints: Machine availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Machine_{m}_Availability"

# Solve the problem
problem.solve()

# Extract results
optimal_batches = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output the result
output = {
    "batches": optimal_batches,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')