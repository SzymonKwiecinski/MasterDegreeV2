import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Number of parts and machines
P = len(data['prices'])
M = len(data['machine_costs'])

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
cost = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))
problem += profit - cost

# Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]

# Solve the problem
problem.solve()

# Output results
for p in range(P):
    print(f'Batches produced for part {p + 1}: {pulp.value(batches[p])}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')