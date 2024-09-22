import pulp

# Data from the provided JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Number of parts (P) and machines (M)
P = len(data['prices'])
M = len(data['availability'])

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{p+1}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]

# Objective function
total_profit = pulp.lpSum([(data['prices'][p] - pulp.lpSum([data['time_required'][m][p] * data['machine_costs'][m] for m in range(M)])) * x[p] for p in range(P)])
problem += total_profit

# Constraints

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) <= data['availability'][m], f'Availability_Constraint_{m+1}'

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')