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

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Constants
P = len(data['prices'])  # number of parts
M = len(data['machine_costs'])  # number of machines

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: Maximize total profit
total_profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
               pulp.lpSum(pulp.lpSum(data['time_required'][m][p] * data['machine_costs'][m] * batches[p] for p in range(P)) for m in range(M))

problem += total_profit

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], f"Machine_availability_{m}"

# Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_batches_{p}"

# Profit constraint
problem += total_profit >= data['min_profit'], "Min_profit"

# Solve the problem
problem.solve()

# Collect results
result_batches = [batches[p].varValue for p in range(P)]
total_profit_value = pulp.value(problem.objective)

# Output
output = {
    "batches": result_batches,
    "total_profit": total_profit_value
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')