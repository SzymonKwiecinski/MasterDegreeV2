import pulp
import json

# Input data
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

# Problem setup
P = len(min_batches)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: Number of batches for each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Objective function: Maximize profit
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - pulp.lpSum(
    [machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) / 100 for m in range(M)]
)
problem += profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Shared availability for machine M and M-1
if M > 1:
    problem += pulp.lpSum([time_required[M-1][p] * batches[p] for p in range(P)]) + pulp.lpSum([time_required[M-2][p] * batches[p] for p in range(P)]) <= availability[M-1] + availability[M-2]

# Solve the problem
problem.solve()

# Results
batches_solution = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "batches": batches_solution,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')