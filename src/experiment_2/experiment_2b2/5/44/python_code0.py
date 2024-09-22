import pulp

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

M = len(machine_costs)  # Number of machines
P = len(prices)  # Number of parts

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[p] - pulp.lpSum([time_required[m][p] * machine_costs[m] for m in range(M)])) * batches[p] for p in range(P)])
problem += profit

# Constraints:
# 1. Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Machine_{m}_Availability"

# Solve the problem
problem.solve()

# Extracting the results
batches_result = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Prepare the output
output = {
    "batches": batches_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')