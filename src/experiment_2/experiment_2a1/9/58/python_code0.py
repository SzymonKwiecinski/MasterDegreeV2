import json
import pulp

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'setup_time': [12, 8, 4, 0]}

# Extracting data from JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective function
profit = pulp.lpSum([(prices[p] * batches[p]) for p in range(P)]) - \
         pulp.lpSum([(machine_costs[m] * pulp.lpSum([(time_required[m][p] * batches[p]) for p in range(P)])) for m in range(M)])
problem += profit

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum([(time_required[m][p] * batches[p]) for p in range(P)]) <= availability[m], f"Machine_Availability_{m}"

# Setup time constraint for machine 1
for p in range(P):
    problem += batches[p] <= 100 * (1 + setup_flags[p])  # Enables setup flag only when producing at least one batch

# Setup time for machine 1
problem += pulp.lpSum([setup_time[p] * setup_flags[p] for p in range(P)]) <= availability[0], "Setup_Time_Machine_1"

# Solve the problem
problem.solve()

# Output results
batches_result = [int(batches[p].varValue) for p in range(P)]
setup_flags_result = [int(setup_flags[p].varValue) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "batches": batches_result,
    "setup_flags": setup_flags_result,
    "total_profit": total_profit
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')