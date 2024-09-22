import pulp
import json

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10]}

# Extracting parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[p] - pulp.lpSum([machine_costs[m] * time_required[m][p] * batches[p] / 100 for m in range(M)])) * batches[p] for p in range(P)])
problem += profit

# Constraints
# Minimum batches constraint
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Availability constraints for machines
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Solve the problem
problem.solve()

# Collecting results
result_batches = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "batches": result_batches,
    "total_profit": total_profit
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')