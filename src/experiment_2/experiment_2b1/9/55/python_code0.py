import pulp
import json

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'standard_cost': 20,
    'overtime_cost': 30,
    'overtime_hour': 400,
    'min_profit': 5000
}

# Define variables
P = len(data['prices'])  # Number of parts
M = len(data['time_required'])  # Number of machines
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Objective function: Maximize total profit
total_profit = pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)]) - \
               pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) for m in range(M)])

problem += total_profit

# Constraints
# Minimum batches constraint
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) <= data['availability'][m]

# Profit constraint
problem += total_profit >= data['min_profit']

# Solve the problem
problem.solve()

# Output results
result_batches = [batches[p].varValue for p in range(P)]
total_profit_value = pulp.value(problem.objective)

output = {
    "batches": result_batches,
    "total_profit": total_profit_value
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')