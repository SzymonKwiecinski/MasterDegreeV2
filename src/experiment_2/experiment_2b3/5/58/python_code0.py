import pulp

# Problem data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Extract the data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Derived data
num_machines = len(machine_costs)
num_parts = len(prices)

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f"batches_{p}", lowBound=0, cat='Integer') for p in range(num_parts)]
setup_flags = [pulp.LpVariable(f"setup_flag_{p}", cat='Binary') for p in range(num_parts)]

# Objective function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(num_parts)])
cost = pulp.lpSum([
    pulp.lpSum([time_required[m][p] * batches[p] * machine_costs[m] for p in range(num_parts)]) +
    setup_flags[p] * setup_time[p] * machine_costs[0]
    for m in range(num_machines)
])
problem += profit - cost

# Constraints
for m in range(num_machines):
    problem += pulp.lpSum([
        time_required[m][p] * batches[p] for p in range(num_parts)
    ]) <= availability[m]

for p in range(num_parts):
    problem += setup_flags[p] >= batches[p] / 100  # if we produce any part, setup must be done

# Solve the problem
problem.solve()

# Output format
result = {
    "batches": [pulp.value(batches[p]) for p in range(num_parts)],
    "setup_flags": [pulp.value(setup_flags[p]) for p in range(num_parts)],
    "total_profit": pulp.value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')