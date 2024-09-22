import pulp
import json

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'setup_time': [12, 8, 4, 0]}

# Parsing input data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[p] * batches[p]) for p in range(P)]) - pulp.lpSum(
    [pulp.lpSum([(machine_costs[m] * time_required[m][p] * batches[p]) for p in range(P)]) for m in range(M)]
)
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum([(time_required[m][p] * batches[p]) for p in range(P)]) <= availability[m]

for p in range(P):
    problem += batches[p] <= 1000 * setup_flags[p]  # Ensure batches only produced if setup is done
    if m == 0:  # Setup time only for machine 1
        problem += setup_flags[p] * setup_time[p] <= availability[0]  # Setup time constraint

# Solve the problem
problem.solve()

# Collect results
batches_result = [pulp.value(batches[p]) for p in range(P)]
setup_flags_result = [pulp.value(setup_flags[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output results
output = {
    "batches": batches_result,
    "setup_flags": setup_flags_result,
    "total_profit": total_profit
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')