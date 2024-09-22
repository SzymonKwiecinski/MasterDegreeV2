import pulp

# Input data
data = {
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "setup_time": [12, 8, 4, 0]
}

# Extracting data
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
batches = [pulp.LpVariable(f'batch_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Objective function: Maximize total profit
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
machine_cost = pulp.lpSum(
    machine_costs[m] * (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) +
                        (setup_flags[p] * setup_time[p] if m == 0 else 0)) 
    for m in range(M))
problem += profit - machine_cost, "Total Profit"

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + (
        pulp.lpSum(setup_flags[p] * setup_time[p] for p in range(P)) if m == 0 else 0) <= availability[m]

# Setup flag constraints
for p in range(P):
    problem += batches[p] <= 10000 * setup_flags[p] # Large number to enforce logical relation

# Solve the problem
problem.solve()

# Output results
output = {
    "batches": [int(batches[p].varValue) for p in range(P)],
    "setup_flags": [int(setup_flags[p].varValue) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')