import pulp

# Data
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]

# Parameters
P = len(prices)
M = len(machine_costs)

# Initialize the problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p+1}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective function
total_profit = pulp.lpSum([
    prices[p] * batches[p] - pulp.lpSum([
        machine_costs[m] * (time_required[m][p] * batches[p] / 100) for m in range(M)
    ]) for p in range(P)
])

problem += total_profit

# Constraints
# Production Constraints
for p in range(P):
    problem += batches[p] >= min_batches[p], f"MinBatchesConstraint_{p+1}"

# Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"MachineAvailabilityConstraint_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')