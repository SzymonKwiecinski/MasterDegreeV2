import pulp

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10], 
    'extra_costs': [0, 15, 22.5], 
    'max_extra': [0, 80, 80]
}

# Extracted data for convenience
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

M = len(machine_costs)  # Number of machines
P = len(prices)         # Number of parts

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0, upBound=max_extra[m], cat='Continuous') for m in range(M)]

# Objective function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
machine_usage_cost = pulp.lpSum([machine_costs[m] * (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)])) for m in range(M)])
extra_time_cost = pulp.lpSum([extra_costs[m] * extra_time[m] for m in range(M)])

problem += profit - (machine_usage_cost + extra_time_cost)

# Constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m] + extra_time[m]

# Solve the problem
problem.solve()

# Results
batches_result = [int(pulp.value(batches[p])) for p in range(P)]
extra_time_result = [pulp.value(extra_time[m]) for m in range(M)]
total_profit = pulp.value(problem.objective)

# Output formatted
output = {
    "batches": batches_result,
    "extra_time": extra_time_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')