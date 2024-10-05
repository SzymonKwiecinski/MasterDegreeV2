import pulp

# Load data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

M = len(time_required)  # Number of machines
P = len(prices)         # Number of parts

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_{p}', cat='Binary') for p in range(P)]

# Objective function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) \
         - pulp.lpSum([machine_costs[m] * (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) + (setup_flags[p] * setup_time[p] if p < P else 0)) for p in range(P)]) for m in range(M)])
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) \
               + pulp.lpSum([setup_flags[p] * setup_time[p] for p in range(P)]) <= availability[m]

# Setup constraints for indicating if a setup is required
for p in range(P):
    problem += batches[p] <= 1000 * setup_flags[p]

# Solve the problem
problem.solve()

# Retrieve results
output_data = {
    "batches": [int(batches[p].varValue) for p in range(P)],
    "setup_flags": [int(setup_flags[p].varValue) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(output_data)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')