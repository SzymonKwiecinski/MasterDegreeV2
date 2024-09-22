import pulp
import json

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
        'machine_costs': [160, 10, 15],
        'availability': [200, 300, 500],
        'prices': [570, 250, 585, 430],
        'setup_time': [12, 8, 4, 0]}

# Extract parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Setup constraints
for p in range(P):
    # If we produce batches of part p, we need to account for setup times
    for m in range(1):  # Only machine 1 has setup time
        problem += batches[p] <= setup_flags[p] * (availability[m] // setup_time[p])

# Solve the problem
problem.solve()

# Prepare output
batches_values = [batches[p].varValue for p in range(P)]
setup_flags_values = [setup_flags[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_values,
    "setup_flags": setup_flags_values,
    "total_profit": total_profit
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')