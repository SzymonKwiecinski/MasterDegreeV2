import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Define problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Constants
P = len(data['prices'])
M = len(data['machine_costs'])

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0) for p in range(P)]

# Objective function
profit = sum(data['prices'][p] * batches[p] for p in range(P))
cost = sum(
    data['machine_costs'][m] * sum(data['time_required'][m][p] * batches[p] for p in range(P))
    for m in range(M)
)
problem += profit - cost

# Machine availability constraints
for m in range(M):
    problem += sum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]

# Sharing availability for Machine M and Machine M-1
problem += (
    sum(data['time_required'][M-1][p] * batches[p] for p in range(P)) +
    sum(data['time_required'][M-2][p] * batches[p] for p in range(P))
    <= data['availability'][M-1] + data['availability'][M-2]
)

# Minimum production requirement for each part
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Solve the problem
problem.solve()

# Output the solution
for p in range(P):
    print(f'Batches of part {p+1}: {batches[p].varValue}')

print(f'Total Profit (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')