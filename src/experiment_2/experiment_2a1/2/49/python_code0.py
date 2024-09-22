import pulp
import json

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Define problem
P = len(data['prices'])
M = len(data['time_required'])
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum((data['prices'][p] - pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] / 100) for m in range(M)) * batches[p] for p in range(P))
problem += profit

# Constraints
# Minimum batches constraint
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Availability constraint: sharing between machine M and M-1
total_time_used = pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P) for m in range(M))
problem += total_time_used <= pulp.lpSum(data['availability'][m] for m in range(M))

# Solve the problem
problem.solve()

# Prepare output
output = {
    "batches": [batches[p].varValue for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

# Print results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')