import pulp

# Extract data from the JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

num_machines = len(time_required)
num_parts = len(time_required[0])

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batch_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(num_parts)]

# Objective Function: Maximize profit
# Profit = Revenue - Cost
revenue = pulp.lpSum([prices[p] * batches[p] for p in range(num_parts)])
costs = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) for m in range(num_machines)])
problem += revenue - costs

# Constraints: Machine hours
for m in range(num_machines):
    if m < num_machines - 2:  # For machine M and M-1 availability is shared
        problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) <= availability[m]

# Availability sharing between last two machines (Machine M and M-1 can share availability)
problem += pulp.lpSum([time_required[m][p] * batches[p] for m in range(num_machines - 2, num_machines) for p in range(num_parts)]) <= sum(availability[-2:])

# Solve the problem
problem.solve()

# Prepare the result
batches_solution = [pulp.value(batches[p]) for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

# Output the solution
solution = {
    "batches": batches_solution,
    "total_profit": total_profit
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')