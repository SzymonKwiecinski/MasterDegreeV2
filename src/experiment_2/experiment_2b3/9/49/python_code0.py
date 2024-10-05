import pulp

# Data provided
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

M = len(machine_costs)
P = len(prices)

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective Function
profit = pulp.lpSum([batches[p] * (prices[p] - pulp.lpSum([machine_costs[m] * time_required[m][p] for m in range(M)])) for p in range(P)])
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Special condition for machine M and M-1 (can share availability)
problem += pulp.lpSum([time_required[M-1][p] * batches[p] for p in range(P)]) + pulp.lpSum([time_required[M-2][p] * batches[p] for p in range(P)]) <= availability[M-1] + availability[M-2]

# Solving the problem
problem.solve()

# Output
result = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')