import pulp

# Data provided
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

P = len(prices)   # Number of parts
M = len(availability)  # Number of machines

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flags_{p}', cat='Binary') for p in range(P)]

# Objective function: Maximize profit
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * (
             pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
             (setup_time[p] * setup_flags[p] if m == 0 else 0)) for m in range(M)])
problem += profit

# Constraints
# Availability constraints for each machine
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + \
               (pulp.lpSum(setup_time[p] * setup_flags[p] for p in range(P)) if m == 0 else 0) <= availability[m]

# Linking setup flags with batches
for p in range(P):
    problem += batches[p] <= availability[0] * setup_flags[p]

# Solve the problem
problem.solve()

# Output values
batches_produced = [pulp.value(batches[p]) for p in range(P)]
setup_flags_output = [pulp.value(setup_flags[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_produced,
    "setup_flags": setup_flags_output,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')