import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

M = len(machine_costs)  # Number of machines
P = len(prices)         # Number of parts

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Objective function
profit = pulp.lpSum([batches[p] * (prices[p] - pulp.lpSum(time_required[m][p] * machine_costs[m] for m in range(M))) for p in range(P)])
problem += profit

# Constraints
for m in range(M-2):
    problem += pulp.lpSum(batches[p] * time_required[m][p] for p in range(P)) <= availability[m]

# Machine M and M-1 shared constraint
problem += pulp.lpSum(batches[p] * (time_required[M-1][p] + time_required[M-2][p]) for p in range(P)) <= (availability[M-1] + availability[M-2])

# Solve the problem
problem.solve()

# Output
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')