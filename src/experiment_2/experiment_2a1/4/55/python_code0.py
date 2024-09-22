import pulp
import json

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10], 
        'standard_cost': 20, 
        'overtime_cost': 30, 
        'overtime_hour': 400, 
        'min_profit': 5000}

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Variables
num_parts = len(data['min_batches'])
batches = pulp.LpVariable.dicts("batches", range(num_parts), lowBound=0, cat='Integer')

# Objective Function
profit = pulp.lpSum((data['prices'][p] * batches[p] - 
                     pulp.lpSum(data['time_required'][m][p] * 
                                 (data['machine_costs'][m] * (data['availability'][m] / sum(data['time_required'][m][p] for p in range(num_parts)) if sum(data['time_required'][m][p] for p in range(num_parts)) > 0 else 1))
                                 )) for m in range(len(data['availability']))) for p in range(num_parts))

problem += profit

# Constraints
for p in range(num_parts):
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_{p}"

total_time = pulp.lpSum(data['time_required'][m][p] * batches[p] for m in range(len(data['availability'])) for p in range(num_parts))

for m in range(len(data['availability'])):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(num_parts)) <= data['availability'][m], f"Machine_Availability_{m}"

# Calculate total cost and profit condition
total_cost = pulp.lpSum((data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(num_parts))) for m in range(len(data['machine_costs'])))
total_profit = profit - total_cost

problem += total_profit >= data['min_profit'], "Min_Profit"

# Solve the problem
problem.solve()

# Output results
batches_result = [pulp.value(batches[p]) for p in range(num_parts)]
total_profit_result = pulp.value(problem.objective)

output = {
    "batches": batches_result,
    "total_profit": total_profit_result
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')