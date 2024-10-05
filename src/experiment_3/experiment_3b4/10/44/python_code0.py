import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Number of products and machines
P = len(data['prices'])
M = len(data['machine_costs'])

# Initialize the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0) for p in range(P)]

# Objective function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P)) - pulp.lpSum(
    data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P))
    for m in range(M)
)

problem += profit

# Constraints: Machine availability
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m]

# Constraints: Minimum batches
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')