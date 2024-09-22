import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Indices
P = len(data['prices'])
M = len(data['machine_costs'])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", (range(P)), lowBound=0, cat='Continuous')
setup_flags = pulp.LpVariable.dicts("setup_flags", (range(P)), cat='Binary')

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
costs = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))
problem += profit - costs

# Constraints

# Machine usage constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]

# Setup time constraints for machine 1
for p in range(P):
    problem += setup_flags[p] * data['setup_time'][p] <= pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P))

# Solve
problem.solve()

# Results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

for p in range(P):
    print(f'Batches of part {p+1}: {batches[p].varValue}, Setup Flag: {setup_flags[p].varValue}')