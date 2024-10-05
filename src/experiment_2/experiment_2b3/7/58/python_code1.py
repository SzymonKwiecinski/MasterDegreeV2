import pulp

# Data Input
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'setup_time': [12, 8, 4, 0]
}

time_required = data["time_required"]
machine_costs = data["machine_costs"]
availability = data["availability"]
prices = data["prices"]
setup_time = data["setup_time"]

M = len(time_required)
P = len(prices)

# Model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
batches = [pulp.LpVariable(f"batches_{p}", lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f"setup_flag_{p}", cat='Binary') for p in range(P)]

# Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
machine_cost = pulp.lpSum([
    machine_costs[m] * (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) +
    (setup_flags[p] * setup_time[p] if m == 0 else 0)) 
    for p in range(P)  # Moved inside this loop
]) for m in range(M)])
problem += profit - machine_cost

# Constraints
for m in range(M):
    problem += pulp.lpSum([
        time_required[m][p] * batches[p] for p in range(P)
    ]) + (pulp.lpSum([setup_flags[p] * setup_time[p] for p in range(P)]) if m == 0 else 0) <= availability[m]

# Solve
problem.solve()

# Results
batches_result = [pulp.value(batches[p]) for p in range(P)]
setup_flags_result = [pulp.value(setup_flags[p]) for p in range(P)]

output = {
    "batches": batches_result,
    "setup_flags": setup_flags_result,
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')