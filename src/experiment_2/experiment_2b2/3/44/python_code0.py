import pulp

# Extracting data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}

time_required = data["time_required"]
machine_costs = data["machine_costs"]
availability = data["availability"]
prices = data["prices"]
min_batches = data["min_batches"]

M = len(machine_costs)
P = len(prices)

# Creating the LP Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: Number of batches for each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Objective Function: Maximize profit
profit = pulp.lpSum([batches[p] * prices[p] for p in range(P)]) - pulp.lpSum([
    pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) * machine_costs[m] for m in range(M)])

problem += profit

# Constraints: Machine availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Solving the problem
problem.solve()

# Extracting results
batches_result = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "batches": batches_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')