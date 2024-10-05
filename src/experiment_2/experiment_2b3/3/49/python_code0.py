import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

time_required = data["time_required"]
machine_costs = data["machine_costs"]
availability = data["availability"]
prices = data["prices"]
min_batches = data["min_batches"]

# Number of parts and machines
P = len(prices)
M = len(time_required)

# Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Objective function
total_revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
total_cost = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))
problem += total_revenue - total_cost

# Constraints

# Global availability constraint for machines M and M-1 (combined)
problem += pulp.lpSum(time_required[M-1][p] * batches[p] for p in range(P)) + \
           pulp.lpSum(time_required[M-2][p] * batches[p] for p in range(P)) <= availability[M-1], f"Shared_Availability"

# Constraints for other machines
for m in range(M - 2):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Availability_{m}"

# Solve the problem
problem.solve()

# Collect results
solution = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')