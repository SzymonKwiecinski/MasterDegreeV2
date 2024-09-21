import pulp

# Data from the provided JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Decision Variables
x = [pulp.LpVariable(f'x_{p}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]

# Problem
problem = pulp.LpProblem("Batch_Production_Problem", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P))
costs = pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] * x[p] for m in range(M) for p in range(P))
problem += profit - costs

# Constraints
# Machine time availability constraint
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')