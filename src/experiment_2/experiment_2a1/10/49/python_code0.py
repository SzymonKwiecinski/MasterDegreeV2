import pulp
import json

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10]}

# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of machines and parts
M = len(machine_costs)
P = len(prices)

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[p] - pulp.lpSum([time_required[m][p] * machine_costs[m] for m in range(M)])) * batches[p] for p in range(P)])
problem += profit

# Constraints
# Minimum batches constraint
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Availability constraints (shared availability for machine M and M-1)
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Solve the problem
problem.solve()

# Collect results
batches_results = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output results
output = {
    "batches": batches_results,
    "total_profit": total_profit
}

print(json.dumps(output))

# Print objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')