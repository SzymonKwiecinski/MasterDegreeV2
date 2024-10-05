import pulp

# Input data
data = {
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "setup_time": [12, 8, 4, 0]
}

# Extract data
time_required = data["time_required"]
machine_costs = data["machine_costs"]
availability = data["availability"]
prices = data["prices"]
setup_time = data["setup_time"]

P = len(prices)  # Number of parts
M = len(availability)  # Number of machines

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_{p}', cat='Binary') for p in range(P)]

# Objective function
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
setup_costs = pulp.lpSum(machine_costs[0] * setup_flags[p] * setup_time[p] for p in range(P))
operating_costs = pulp.lpSum(machine_costs[m] * time_required[m][p] * batches[p] for m in range(M) for p in range(P))

profit = revenue - setup_costs - operating_costs
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

for p in range(P):
    problem += batches[p] >= setup_flags[p]  # Setup flag should be 1 if a part is produced

# Solve the problem
problem.solve()

# Output results
result = {
    "batches": [batches[p].varValue for p in range(P)],
    "setup_flags": [setup_flags[p].varValue for p in range(P)],
    "total_profit": pulp.value(profit)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')