import pulp

# Data from JSON
data = {
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "setup_time": [12, 8, 4, 0]
}

time_required = data["time_required"]
machine_costs = data["machine_costs"]
availability = data["availability"]
prices = data["prices"]
setup_time = data["setup_time"]

M = len(machine_costs)
P = len(prices)

# Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Objective function
revenue = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
machine_cost = pulp.lpSum([
    pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) * machine_costs[m] + 
    (setup_flags[p] * setup_time[p] if m == 0 else 0) * machine_costs[m]
    for p in range(P) for m in range(M)
])
profit = revenue - machine_cost
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) + \
               (setup_flags[p] * setup_time[p] if m == 0 else 0) <= availability[m]

# Solve the problem
problem.solve()

# Results
output = {
    "batches": [int(batches[p].varValue) for p in range(P)],
    "setup_flags": [int(setup_flags[p].varValue) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')