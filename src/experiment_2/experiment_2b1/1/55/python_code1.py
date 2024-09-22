import pulp
import json

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10], 
        'standard_cost': 20, 
        'overtime_cost': 30, 
        'overtime_hour': 400, 
        'min_profit': 5000}

# Extracting data from json
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective function (total profit)
total_profit = pulp.lpSum(
    (prices[p] * batches[p] - 
     pulp.lpSum(time_required[m][p] * batches[p] * machine_costs[m] for m in range(M)))
    for p in range(P)
)
)
problem += total_profit

# Constraints

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum((time_required[m][p] * batches[p]) for p in range(P)) <= availability[m]

# Minimum batches required for each part
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Profit constraint
problem += total_profit >= min_profit

# Solve the problem
problem.solve()

# Gather results
result_batches = [batches[p].varValue for p in range(P)]
total_profit_value = pulp.value(problem.objective)

# Output the result
output = {
    "batches": result_batches,
    "total_profit": total_profit_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')