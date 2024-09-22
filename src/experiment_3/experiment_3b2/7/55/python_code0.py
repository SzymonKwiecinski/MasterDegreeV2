import pulp
import json

# Data provided in JSON format
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

# Decision variables
P = len(data['prices'])
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)

# Create the model
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Objective function
profit = pulp.lpSum([data['prices'][p] * x[p] for p in range(P)]) \
         - pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) for m in range(1, len(data['machine_costs']))]) \
         - (data['standard_cost'] * pulp.lpMin(data['overtime_hour'], pulp.lpSum([data['time_required'][0][p] * x[p] for p in range(P)])) \
         + data['overtime_cost'] * pulp.lpMax(0, pulp.lpSum([data['time_required'][0][p] * x[p] for p in range(P)]) - data['overtime_hour']))

problem += profit, "Total_Profit"

# Constraints
# Machine availability constraints
for m in range(1, len(data['availability'])):
    problem += (pulp.lpSum([data['time_required[m][p] * x[p] for p in range(P)]]) <= data['availability'][m]), f"Machine_Availability_{m}"

# Minimum production requirement for each part
for p in range(P):
    problem += (x[p] >= data['min_batches'][p]), f"Min_Batches_{p}"

# Profit constraint
problem += (profit >= data['min_profit']), "Min_Profit"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')