import pulp
import json

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Extract data from json
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Constants
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective function
profit = pulp.lpSum((prices[p] * batches[p]) for p in range(P)) - pulp.lpSum(
    (machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P))) for m in range(M)
)

problem += profit

# Constraints
# Each machine's availability constraint
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Setup time constraint for machine 1 (only if a part is produced)
for p in range(P):
    problem += batches[p] <= 1000 * setup_flags[p]  # Ensure that setup is only when batches are made
    if m == 0:
        problem += setup_flags[p] * setup_time[p] <= availability[m]

# Solve the problem
problem.solve()

# Retrieve results
batches_result = [batches[p].varValue for p in range(P)]
setup_flags_result = [setup_flags[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "batches": batches_result,
    "setup_flags": setup_flags_result,
    "total_profit": total_profit
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')