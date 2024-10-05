import pulp

# Data from JSON
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]

# Indices
P = len(prices)
M = len(machine_costs)

# Problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
costs = pulp.lpSum(machine_costs[m] * (time_required[m][p] / 100) * batches[p] for m in range(M) for p in range(P))
problem += profit - costs

# Constraints

# Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum((time_required[m][p] / 100) * batches[p] for p in range(P)) <= availability[m], f'Availability_Constraint_{m}'

# Minimum Production Requirement Constraints
for p in range(P):
    problem += batches[p] >= min_batches[p], f'Minimum_Batches_Constraint_{p}'

# Solve the problem
problem.solve()

# Output the results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')