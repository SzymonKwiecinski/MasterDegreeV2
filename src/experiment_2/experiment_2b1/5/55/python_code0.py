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

# Problem parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Define variables
num_parts = len(prices)
batches = pulp.LpVariable.dicts("Batches", range(num_parts), lowBound=0, cat='Integer')

# Define objective function: total profit
profit = pulp.lpSum((prices[p] - pulp.lpSum(time_required[m][p] * machine_costs[m] for m in range(len(machine_costs)))) * batches[p] for p in range(num_parts))
problem += profit

# Constraints
# Minimum batches constraint
for p in range(num_parts):
    problem += batches[p] >= min_batches[p]

# Machine availability constraints
for m in range(len(availability)):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m]

# Total profit constraint
problem += profit >= min_profit

# Solve the problem
problem.solve()

# Prepare output
batches_result = [int(batches[p].varValue) for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')