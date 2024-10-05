import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Indices
P = len(data['prices'])
M = len(data['machine_costs'])

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
profit = pulp.lpSum([data['prices'][p] * x[p] for p in range(P)])
machine_costs = pulp.lpSum([data['time_required'][m][p] * x[p] * data['machine_costs'][m] for p in range(P) for m in range(M)])
problem += profit - machine_costs

# Constraints

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) <= data['availability'][m], f"Machine_availability_{m}"

# Minimum production requirement constraints
for p in range(P):
    problem += x[p] >= data['min_batches'][p], f"Min_batches_{p}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')