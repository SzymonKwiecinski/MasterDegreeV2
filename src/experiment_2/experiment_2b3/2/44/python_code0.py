import pulp

# Extracting data from JSON format
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10]}

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

M = len(time_required)  # Number of machines
P = len(time_required[0])  # Number of parts

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
revenue = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
cost = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])
profit = revenue - cost
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Solve
problem.solve()

# Results
result_batches = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(profit)

# Output format
output = {
    "batches": result_batches,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')