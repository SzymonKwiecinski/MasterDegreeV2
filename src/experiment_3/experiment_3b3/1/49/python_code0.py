import pulp

# Data provided in JSON format
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

# Initialize the problem
problem = pulp.LpProblem("AutoPartsManufacturing", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
profit = pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit

# Constraints

# Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) <= data['availability'][m]

# Minimum Production Requirements
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Solve the problem
problem.solve()

# Print the results
for p in range(P):
    print(f'Batches for Part {p+1}: {batches[p].varValue}')

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')