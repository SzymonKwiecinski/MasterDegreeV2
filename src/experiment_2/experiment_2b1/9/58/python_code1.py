import pulp
import json

# Data input
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Extracting data from the input
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Problem setup
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Objective function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - pulp.lpSum(
    [machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)]
)
problem += profit

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Setup condition
for p in range(P):
    problem += batches[p] <= setup_flags[p] * 10000  # Using a large number instead of lpInf

# Total setup time constraint for machine 1
problem += pulp.lpSum([setup_time[p] * setup_flags[p] for p in range(P)]) <= availability[0]

# Solve the problem
problem.solve()

# Prepare output
result = {
    "batches": [int(batches[p].varValue) for p in range(P)],
    "setup_flags": [int(setup_flags[p].varValue) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

# Display the result
print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')