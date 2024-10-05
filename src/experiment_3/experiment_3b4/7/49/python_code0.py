import pulp

# Data
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the LP problem
problem = pulp.LpProblem("AutoPartsManufacturing", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'x_{p+1}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
machining_cost = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit - machining_cost

# Constraints

# Machine availability constraints for M-2 machines
for m in range(M - 2):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Combined machine availability for machines M and M-1
problem += pulp.lpSum([time_required[M-1][p] * batches[p] for p in range(P)]) + pulp.lpSum([time_required[M-2][p] * batches[p] for p in range(P)]) <= availability[M-1] + availability[M-2]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')