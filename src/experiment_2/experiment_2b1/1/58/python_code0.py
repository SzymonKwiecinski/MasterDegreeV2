import pulp
import json

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'setup_time': [12, 8, 4, 0]}

# Extracting data from the input
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Define variables
P = len(prices)  # number of parts
M = len(machine_costs)  # number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - pulp.lpSum([
    machine_costs[m] * pulp.lpSum([
        time_required[m][p] * batches[p] for p in range(P)
    ]) for m in range(M)
])

problem += profit

# Constraints for machine availability
for m in range(M):
    problem += (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) +
                 pulp.lpSum([setup_flags[p] * setup_time[p] for p in range(P)]) <= availability[m])

# Setup constraints
for p in range(P):
    for m in range(M):
        if m == 0:  # Only machine 1 requires setup time
            problem += (batches[p] <= 1000 * setup_flags[p])  # Ensure batches only if setup

# Solve the problem
problem.solve()

# Collect the results
result_batches = [batches[p].varValue for p in range(P)]
result_setup_flags = [setup_flags[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output the result
output = {
    "batches": result_batches,
    "setup_flags": result_setup_flags,
    "total_profit": total_profit
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')