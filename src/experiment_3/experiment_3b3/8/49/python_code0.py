import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Problem Setup
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batch_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
cost = pulp.lpSum([machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M)])
problem += profit - cost

# Constraints
# Availability Constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Minimum Production Requirements
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Solving the problem
problem.solve()

# Output results
batches_result = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'Batch production: {batches_result}')
print(f'Total Profit (Objective Value): <OBJ>{total_profit}</OBJ>')