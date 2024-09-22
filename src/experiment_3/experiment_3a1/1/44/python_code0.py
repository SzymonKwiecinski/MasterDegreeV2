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

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Decision variables
b = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective function
profit = pulp.lpSum([prices[p] * b[p] for p in range(P)]) - pulp.lpSum(
    [
        machine_costs[m] * pulp.lpSum([time_required[m][p] * b[p] for p in range(P)])
        for m in range(M)
    ]
)

problem += profit

# Constraints for machine availability
for m in range(M):
    problem += (
        pulp.lpSum([time_required[m][p] * b[p] for p in range(P)]) <= availability[m]
    )

# Constraints for minimum production requirements
for p in range(P):
    problem += b[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Output results
batches = [b[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'batches = {batches}')
print(f'total_profit = {total_profit}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')