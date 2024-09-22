import pulp

# Data input
data = {
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10]
}

# Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

M = len(time_required)  # Number of machines
P = len(prices)  # Number of parts

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches for each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Objective function: Maximize profit
# Profit = Revenue - Machine Costs
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
machine_usage_costs = pulp.lpSum(
    machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P))
    for m in range(M)
)
profit = revenue - machine_usage_costs
problem += profit

# Constraints for available time on the machines,
# with machines M and M-1 sharing availability
for m in range(M-2):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Special availability constraint for machines M and M-1 being shared
problem += (
    pulp.lpSum(time_required[M-1][p] * batches[p] for p in range(P)) +
    pulp.lpSum(time_required[M-2][p] * batches[p] for p in range(P))
    <= availability[M-1]  # total shared availability
)

# Solve the problem
problem.solve()

# Construct output
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')