import pulp

# Define the input data
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

M = len(time_required)
P = len(time_required[0])

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches of each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p]) for p in range(P)]

# Objective function: Maximize total profit
total_revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
total_cost = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))
problem += total_revenue - total_cost

# Constraints: Machine availability
for m in range(M - 1):  # For first M-2 machines
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Combined availability constraint for the last two machines
problem += pulp.lpSum(time_required[M-1][p] * batches[p] for p in range(P)) + pulp.lpSum(time_required[M-2][p] * batches[p] for p in range(P)) <= availability[M-1]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

# Print result
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')