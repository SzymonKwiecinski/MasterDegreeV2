import pulp

# Reading data
data = {
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "setup_time": [12, 8, 4, 0]
}

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Constants
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Initializing the model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batch_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Objective function: Maximize Profit
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)]) - \
         pulp.lpSum([setup_flags[p] * machine_costs[0] * setup_time[p] for p in range(P)])

problem += profit, "Total_Profit"

# Constraints
# Machine time availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Avail_Machine_{m}"

# Setup time constraint for machine 1
for p in range(P):
    problem += batches[p] <= availability[0] * setup_flags[p] / (setup_time[p] + 1e-5), f"Setup_Constraint_Part_{p}"

# Solve the problem
problem.solve()

# Output the results
output = {
    "batches": [int(pulp.value(batches[p])) for p in range(P)],
    "setup_flags": [int(pulp.value(setup_flags[p])) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')