import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

# Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches for each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective function: Maximize profit = Revenue - Costs
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
costs = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit - costs

# Constraints: Machine availability
# Adjust by combining last two machines' availability
for m in range(M-2):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Combined availability for the last two machines
combined_availability = availability[M-2] + availability[M-1]
problem += pulp.lpSum([time_required[M-2][p] * batches[p] for p in range(P)]) <= combined_availability

# Solve the problem
problem.solve()

# Extract results
batches_solution = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Print the results in required format
print({
    "batches": batches_solution,
    "total_profit": total_profit
})
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')