import pulp

# Extracting data from JSON
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

# Initialize the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) \
    - pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit

# Constraints

# Machine availability constraints
for m in range(M):
    problem += (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m])

# Shared availability constraint for Machine M and M-1
problem += (pulp.lpSum([time_required[M-2][p] * batches[p] for p in range(P)]) +
            pulp.lpSum([time_required[M-1][p] * batches[p] for p in range(P)]) <= availability[M-2] + availability[M-1])

# Minimum batches requirement
for p in range(P):
    problem += (batches[p] >= min_batches[p])

# Solve the problem
problem.solve()

# Print the optimal value of the objective function
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')