import pulp

# Data from the problem
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Number of parts and machines
P = len(data['prices'])
M = len(data['availability'])

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0, upBound=data['max_extra'][m], cat='Continuous') for m in range(M)]

# Objective function: Maximize profit
profit = pulp.lpSum([batches[p] * data['prices'][p] for p in range(P)])
costs = pulp.lpSum([(pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) + extra_time[m]) * (data['machine_costs'][m] + data['extra_costs'][m]) for m in range(M)])
problem += profit - costs

# Constraints
for m in range(M):
    # Machine time availability constraint
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m] + extra_time[m]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "extra_time": [pulp.value(extra_time[m]) for m in range(M)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')