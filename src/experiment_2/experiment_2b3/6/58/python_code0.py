import pulp

# Data from the problem description
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'setup_time': [12, 8, 4, 0]
}

# Extracting the data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

M = len(machine_costs)  # Number of machines
P = len(prices)         # Number of parts

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Objective function: maximize profit
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)])  # Revenue
costs = pulp.lpSum([time_required[m][p] * batches[p] * machine_costs[m] for m in range(M) for p in range(P)])  # Production cost
setup_cost = pulp.lpSum([setup_time[p] * setup_flags[p] * machine_costs[0] for p in range(P)])  # Setup cost on machine 1

problem += profit - costs - setup_cost, "Total_Profit"

# Constraints: machine availability
for m in range(M):
    problem += pulp.lpSum([(time_required[m][p] * batches[p] + (setup_time[p] * setup_flags[p] if m == 0 else 0)) for p in range(P)]) <= availability[m]

# Ensuring setup flag consistency
for p in range(P):
    problem += batches[p] <= setup_flags[p] * 1e6  # A large constant to link setup flag with batches

# Solve the problem
problem.solve()

# Extract results
batches_produced = [int(batches[p].varValue) for p in range(P)]
setup_flags_result = [int(setup_flags[p].varValue) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output in specified format
output = {
    "batches": batches_produced,
    "setup_flags": setup_flags_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')