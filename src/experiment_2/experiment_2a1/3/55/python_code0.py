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

# Defining the problem
P = len(data['prices'])
M = len(data['time_required'])

# Create a LP problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Decision variables: number of batches for each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective Function: maximize total profit
total_profit = pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)]) - \
               pulp.lpSum([data['machine_costs'][m] * 
                            pulp.lpSum([data['time_required'][m][p] * batches[p] / 100 for p in range(P)]) 
                            for m in range(M)])

problem += total_profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += (pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) <= data['availability'][m]), f"Availability_Constraint_Machine_{m + 1}"

# Minimum batches constraint
for p in range(P):
    problem += (batches[p] >= data['min_batches'][p]), f"Min_Batches_Constraint_Part_{p + 1}"

# Profit constraint
problem += (total_profit >= data['min_profit']), "Min_Profit_Constraint"

# Solving the problem
problem.solve()

# Prepare output
batches_result = [pulp.value(batches[p]) for p in range(P)]
total_profit_value = pulp.value(problem.objective)

# Output
output = {
    "batches": batches_result,
    "total_profit": total_profit_value
}

print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')
print(json.dumps(output))