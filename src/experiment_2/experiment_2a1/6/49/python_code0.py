import pulp
import json

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10]}

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches to produce for each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective function: Maximize total profit = sum(price_p * batches_p) - sum(cost_m * hours_used_m)
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
costs = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] / 100 for p in range(P)) for m in range(M))
problem += profit - costs

# Constraints
# Machine availability constraint
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Minimum batches constraint
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Share availability constraint between Machine M and M-1
if M > 1:
    problem += pulp.lpSum(time_required[M-1][p] * batches[p] for p in range(P)) + \
               pulp.lpSum(time_required[M-2][p] * batches[p] for p in range(P)) <= availability[M-1] + availability[M-2]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "batches": [batches[p].varValue for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')