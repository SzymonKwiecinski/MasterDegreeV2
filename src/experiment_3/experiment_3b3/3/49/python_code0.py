import pulp

# Data from JSON
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')

# Objective function
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
cost = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))
problem += revenue - cost

# Constraints
# Availability constraints for each machine
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Special constraint for sharing machines M and M-1
problem += pulp.lpSum(time_required[M-1][p] * batches[p] for p in range(P)) + pulp.lpSum(time_required[M-2][p] * batches[p] for p in range(P)) <= availability[M-1] + availability[M-2]

# Minimum batches constraint
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')