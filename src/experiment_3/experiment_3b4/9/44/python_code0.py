import pulp

# Data from the problem
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

# Define problem
problem = pulp.LpProblem("AutoPartsManufacturing", pulp.LpMaximize)

# Constants
P = len(data['prices'])
M = len(data['availability'])

# Decision Variables
batches = [pulp.LpVariable(f'batch_{p}', lowBound=0, cat='Integer') for p in range(P)]

# Objective Function
revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
operating_cost = pulp.lpSum(
    data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P))
    for m in range(M)
)
problem += revenue - operating_cost

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]

# Minimum production constraints
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')