import pulp

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}

time_required = data["time_required"]
machine_costs = data["machine_costs"]
availability = data["availability"]
prices = data["prices"]
setup_time = data["setup_time"]

M = len(time_required)  # number of machines
P = len(prices)  # number of parts

# Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
batches = [pulp.LpVariable(f"batches_{p}", lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f"setup_flag_{p}", cat='Binary') for p in range(P)]

# Objective function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
    pulp.lpSum([machine_costs[m] * (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)])) for m in range(M)]) - \
    pulp.lpSum([setup_flags[p] * setup_time[p] * machine_costs[0] for p in range(P)])

problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Setup time constraints for machine 1
for p in range(P):
    problem += batches[p] >= setup_flags[p]

# Solve problem
problem.solve()

# Output results
batches_solution = [int(batches[p].varValue) for p in range(P)]
setup_flags_solution = [int(setup_flags[p].varValue) for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_solution,
    "setup_flags": setup_flags_solution,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')