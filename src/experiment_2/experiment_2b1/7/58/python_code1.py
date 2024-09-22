import json
import pulp

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'setup_time': [12, 8, 4, 0]}

# Problem parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

M = len(machine_costs)  # number of machines
P = len(prices)         # number of parts

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flag_{p}', lowBound=0, upBound=1, cat='Binary') for p in range(P)]

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - pulp.lpSum(
    machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) / 100 for m in range(M)
)
problem += profit

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m] * 100

# Constraints for setup time (only applicable if the part has setup time)
for p in range(P):
    if setup_time[p] > 0:
        problem += batches[p] <= setup_flags[p] * (availability[0] // setup_time[p])
    else:
        problem += batches[p] <= availability[0] * 100  # No setup time means we can produce as much as allowed

# Solve the problem
problem.solve()

# Output
batches_result = [pulp.value(batches[p]) for p in range(P)]
setup_flags_result = [pulp.value(setup_flags[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_result,
    "setup_flags": setup_flags_result,
    "total_profit": total_profit
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')