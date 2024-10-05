import pulp

# Data input
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

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Objective function: Maximize profit
profit_expression = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
cost_expression = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)]) + pulp.lpSum([setup_flags[p] * setup_time[p] for p in range(P)])
problem += (profit_expression - cost_expression), "Total Profit"

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) + pulp.lpSum([setup_flags[p] * setup_time[p] for p in range(P)]) <= availability[m], f"Availability_Constraint_Machine_{m}"

# Machine 1 setup constraint
for p in range(P):
    problem += setup_flags[p] >= batches[p] / 1000, f"Setup_Flag_Constraint_Part_{p}"

# Solve the problem
problem.solve()

# Results
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "setup_flags": [pulp.value(setup_flags[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')