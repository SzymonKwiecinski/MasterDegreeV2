import pulp

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

M = len(machine_costs)
P = len(prices)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Objective function
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
machine_costs_total = pulp.lpSum(
    (time_required[m][p] * batches[p] + (setup_time[p] if m == 0 else 0) * setup_flags[p]) * machine_costs[m]
    for m in range(M) for p in range(P)
)

profit = revenue - machine_costs_total
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum(
        (time_required[m][p] * batches[p] + (setup_time[p] if m == 0 else 0) * setup_flags[p])
        for p in range(P)) <= availability[m]

# Solve the problem
problem.solve()

# Retrieve results
batches_result = [pulp.value(batches[p]) for p in range(P)]
setup_flags_result = [pulp.value(setup_flags[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output dictionary
output = {
    "batches": batches_result,
    "setup_flags": setup_flags_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')