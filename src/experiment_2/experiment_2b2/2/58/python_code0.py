import pulp

# Data received in JSON format
data = {
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "setup_time": [12, 8, 4, 0]
}

# Problem initialization
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Extract data
time_required = data["time_required"]
machine_costs = data["machine_costs"]
availability = data["availability"]
prices = data["prices"]
setup_time = data["setup_time"]

M = len(machine_costs)
P = len(prices)

# Decision variables
batches = [pulp.LpVariable(f"batches_{p}", lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f"setup_flag_{p}", cat='Binary') for p in range(P)]

# Objective function: Maximize profit
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
cost = pulp.lpSum(machine_costs[m] * (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
                 (setup_flags[p] * setup_time[p] if m == 0 else 0)) for m in range(M))
problem += revenue - cost, "Total Profit"

# Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + (
        pulp.lpSum(setup_flags[p] * setup_time[p] for p in range(P)) if m == 0 else 0) <= availability[m], f"Machine_{m}_availability"

# Solve the problem
problem.solve()

# Output the results
solution = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "setup_flags": [pulp.value(setup_flags[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')