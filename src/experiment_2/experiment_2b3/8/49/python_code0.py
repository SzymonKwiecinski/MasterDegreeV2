import pulp

# Parse the input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

M = len(time_required)  # Number of machines
P = len(time_required[0])  # Number of parts

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
batches = [pulp.LpVariable(f"batches_{p}", lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective function
profit = pulp.lpSum([batches[p] * prices[p] for p in range(P)])
costs = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit - costs

# Constraints
# Machine M and M-1 share availability constraint
shared_availability_constraint = pulp.lpSum([time_required[M-1][p] * batches[p] for p in range(P)]) + pulp.lpSum([time_required[M-2][p] * batches[p] for p in range(P)])
problem += shared_availability_constraint <= availability[M-1] + availability[M-2]

# Constraint for other machines
for m in range(M-2):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Solve
problem.solve()

# Result
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')