import pulp

# Input data in JSON format
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

# Problem dimensions
M = len(machine_costs)
P = len(prices)

# Creating the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches for each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective function: Maximize total profit
profit = pulp.lpSum([
    prices[p] * batches[p] -
    pulp.lpSum(time_required[m][p] * machine_costs[m] * batches[p] for m in range(M))
    for p in range(P)
])
problem += profit

# Constraints for machine availability
# Note: machine M and M-1 share availability, constraint will be combined for machine M.
for m in range(M - 1):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]
problem += pulp.lpSum(time_required[M-1][p] * batches[p] for p in range(P)) + \
           pulp.lpSum(time_required[M-2][p] * batches[p] for p in range(P)) <= availability[M-1]

# Solving the problem
problem.solve()

# Collect results
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

# Print output in required format
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')