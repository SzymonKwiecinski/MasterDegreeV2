import json
import pulp

# Input data in JSON format
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'setup_time': [12, 8, 4, 0]}

# Extracting parameters from data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective function: Maximize profit
profit = pulp.lpSum((prices[p] * batches[p] - pulp.lpSum(
    time_required[m][p] * machine_costs[m] * batches[p] / 100 for m in range(M))
) for p in range(P))
problem += profit

# Constraints for machine availability
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m])

# Setup time constraints only for part that requires setup
for p in range(P):
    problem += (setup_flags[p] * setup_time[p] <= pulp.lpSum(batches[p]))

# Add constraints to ensure that batches can only be produced if setup flag is on
for p in range(P):
    problem += (batches[p] <= 1000 * setup_flags[p])  # Arbitrary high value, as there's no minimum

# Solve the problem
problem.solve()

# Output
result = {
    "batches": [int(batches[p].varValue) if batches[p].varValue is not None else 0 for p in range(P)],
    "setup_flags": [int(setup_flags[p].varValue) if setup_flags[p].varValue is not None else 0 for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(f' (Objective Value): <OBJ>{result["total_profit"]}</OBJ>')