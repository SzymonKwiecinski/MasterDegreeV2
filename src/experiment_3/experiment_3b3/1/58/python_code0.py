import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Indices
P = len(data['prices'])
M = len(data['machine_costs'])

# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Problem
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", (range(P)), lowBound=0, cat=pulp.LpContinuous)
setup_flag = pulp.LpVariable.dicts("setup_flag", (range(P)), cat=pulp.LpBinary)

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
cost = pulp.lpSum(
    machine_costs[m] * (
        pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) +
        (pulp.lpSum(setup_time[p] * setup_flag[p] for p in range(P)) if m == 0 else 0)
    ) for m in range(M))
problem += profit - cost

# Constraints
# Machine availability constraints
for m in range(M):
    if m == 0:
        machine_hours = pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + \
                        pulp.lpSum(setup_time[p] * setup_flag[p] for p in range(P))
    else:
        machine_hours = pulp.lpSum(time_required[m][p] * batches[p] for p in range(P))
    problem += machine_hours <= availability[m]

# Solve
problem.solve()

# Output results
print("Batches Produced:")
for p in range(P):
    print(f"Part {p+1}: {pulp.value(batches[p])} batches")

print("Setup Flags:")
for p in range(P):
    print(f"Part {p+1}: {'Set up' if pulp.value(setup_flag[p]) else 'Not set up'}")

print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")