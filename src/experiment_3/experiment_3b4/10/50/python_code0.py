import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)
M = len(machine_costs)

# Problem
problem = pulp.LpProblem("Batch_Maximization", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]
e = [pulp.LpVariable(f'e_{m}', lowBound=0, upBound=max_extra[m], cat='Continuous') for m in range(M)]

# Objective Function
revenue = pulp.lpSum(prices[p] * x[p] for p in range(P))
cost = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) + extra_costs[m] * e[m] for m in range(M))
problem += revenue - cost

# Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m] + e[m]

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')