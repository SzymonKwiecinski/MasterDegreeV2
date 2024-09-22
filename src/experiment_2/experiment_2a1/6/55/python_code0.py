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

# Define problem
problem = pulp.LpProblem("AutoPartsProduction", pulp.LpMaximize)

# Variables
P = len(data['prices'])
M = len(data['time_required'])

# Batches produced for each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective Function: Maximize total profit
total_profit = pulp.lpSum([(data['prices'][p] * batches[p]) for p in range(P)]) - \
               pulp.lpSum([(data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)])) for m in range(M)]) - \
               pulp.lpSum([data['standard_cost'] * (pulp.lpSum([data['time_required'][0][p] * batches[p] for p in range(P)]) - data['overtime_hour']) for p in range(P) if (pulp.lpSum([data['time_required'][0][p] * batches[p] for p in range(P)]) > data['overtime_hour']) else 0]) - \
               pulp.lpSum([data['overtime_cost'] * (pulp.lpSum([data['time_required'][0][p] * batches[p] for p in range(P)]) - data['overtime_hour']) for p in range(P) if (pulp.lpSum([data['time_required'][0][p] * batches[p] for p in range(P)]) > data['overtime_hour']) else 0])

problem += total_profit

# Constraints
# Minimum batches for each part
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"MinBatchesPart{p}"

# Availability constraints for each machine
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) <= data['availability'][m], f"AvailabilityMachine{m}"

# Profit constraint
problem += total_profit >= data['min_profit'], "MinProfit"

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