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

# Problem setup
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum((prices[p] * batches[p] - 
                     pulp.lpSum((time_required[m][p] * machine_costs[m] / 100) * batches[p] 
                                 for m in range(M))) for p in range(P))
problem += profit

# Constraints
# Machine availability constraint
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Minimum batches requirement
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Output
batches_produced = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

result = {
    "batches": batches_produced,
    "total_profit": total_profit
}

# Printing the results
print(json.dumps(result))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')