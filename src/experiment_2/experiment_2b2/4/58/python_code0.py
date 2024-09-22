import pulp

# Problem data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Unpacking data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

M = len(machine_costs)  # Number of machines
P = len(prices)         # Number of parts

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Objective function
profit = pulp.lpSum([prices[p] * batches[p] - pulp.lpSum([time_required[m][p] * machine_costs[m] * batches[p] for m in range(M)]) - setup_flags[p] * machine_costs[0] * setup_time[p] for p in range(P)])
problem += profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Linking setup flags with production
for p in range(P):
    problem += batches[p] <= setup_flags[p] * 1e6  # Use a large number to ensure binary logic works

# Solve the problem
problem.solve()

# Collect results
batches_result = [pulp.value(batches[p]) for p in range(P)]
setup_flags_result = [pulp.value(setup_flags[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Prepare output
output = {
    "batches": batches_result,
    "setup_flags": setup_flags_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')