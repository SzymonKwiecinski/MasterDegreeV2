import json
import pulp

data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

# Extracting the data from the loaded JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[p] - pulp.lpSum([machine_costs[m] * time_required[m][p] for m in range(M)])) * batches[p] for p in range(P)])
problem += profit

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Setup time constraints for machine 1 (only)
for p in range(P):
    problem += (setup_flags[p] * setup_time[p]) + (pulp.lpSum([time_required[m][p] * batches[p] for m in range(M)])) <= availability[0]

# Solving the problem
problem.solve()

# Collecting results
result_batches = [batches[p].varValue for p in range(P)]
result_setup_flags = [setup_flags[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Preparing output
output = {
    "batches": result_batches,
    "setup_flags": result_setup_flags,
    "total_profit": total_profit
}

# Print the result
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')