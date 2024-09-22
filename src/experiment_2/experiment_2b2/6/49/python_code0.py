import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

# Unpack data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
P = len(prices)
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective Function
profit = pulp.lpSum([
    batches[p] * (prices[p] - pulp.lpSum([time_required[m][p] * machine_costs[m] for m in range(len(machine_costs))]))
    for p in range(P)
])
problem += profit, "Total_Profit"

# Constraints for availability with shared availability for Machine M and M-1
for m in range(len(machine_costs) - 2):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Shared availability constraint for Machine M and M-1
problem += pulp.lpSum([time_required[m][-1] * batches[-1] for m in range(len(machine_costs) - 2, len(machine_costs))]) <= sum(availability[-2:])

# Solve
problem.solve()

# Prepare solution output
batches_produced = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

solution = {
    "batches": batches_produced,
    "total_profit": total_profit
}

# Printing solution
print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')