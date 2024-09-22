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

# Initialize the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Variables
P = len(data['prices'])
M = len(data['time_required'])
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['min_batches'][p]) for p in range(P)]

# Objective function
revenue = pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)])
costs = pulp.lpSum([data['machine_costs'][m] * 
                    pulp.lpSum([data['time_required'][m][p] * (batches[p] / 100) for p in range(P)]) for m in range(M)])
profit = revenue - costs

problem += profit

# Constraints
# Machine time availability constraints
for m in range(M):
    problem += (pulp.lpSum([data['time_required'][m][p] * (batches[p] / 100) for p in range(P)]) <= data['availability'][m]), f"availability_constraint_machine_{m+1}"

# Profit constraint
problem += (profit >= data['min_profit']), "min_profit_constraint"

# Solve the problem
problem.solve()

# Output results
batches_result = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_result,
    "total_profit": total_profit
}

# Print objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')