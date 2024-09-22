import pulp

# Data from the provided JSON format
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

# Initialize the LP problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision variables
P = len(data['prices'])
b = pulp.LpVariable.dicts("b", range(P), lowBound=0)

# Objective function
labor_cost_expr = pulp.lpSum([
    (data['standard_cost'] * 
     pulp.lpSum([(time / 100) * b[p] for p, time in enumerate(data['time_required'][0])])) 
     if pulp.lpSum([(time / 100) * b[p] for p, time in enumerate(data['time_required'][0])]) <= data['overtime_hour'] 
     else 
     (data['standard_cost'] * data['overtime_hour'] + data['overtime_cost'] * 
      (pulp.lpSum([(time / 100) * b[p] for p, time in enumerate(data['time_required'][0])]) - data['overtime_hour'])) 
     )
])
profit_expr = pulp.lpSum([data['prices'][p] * b[p] for p in range(P)]) - labor_cost_expr
problem += profit_expr, "Total_Profit"

# Constraints
for m in range(1, len(data['availability'])):
    problem += pulp.lpSum([(data['time_required'][m][p] / 100) * b[p] for p in range(P)]) <= data['availability'][m], f"Machine_Availability_{m}"

for p in range(P):
    problem += b[p] >= data['min_batches'][p], f"Min_Batch_Requirement_{p}"

# Profit requirement constraint
problem += profit_expr >= data['min_profit'], "Min_Profit_Requirement"

# Solve the problem
problem.solve()

# Output the results
for p in range(P):
    print(f'Number of batches produced for part {p+1}: {b[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')