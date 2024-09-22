import pulp

# Data from JSON
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
P = len(data['prices'])
x = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P))
cost_machines = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) for m in range(len(data['machine_costs'])))
c1 = pulp.lpSum(data['time_required'][0][p] * x[p] for p in range(P))

overtime_cost_expr = pulp.lpSum([0, c1 - data['overtime_hour']]) * data['overtime_cost']
c1_expr = pulp.LpAffineExpression([(data['standard_cost'], c1)]) if c1 <= data['overtime_hour'] else pulp.LpAffineExpression([(data['standard_cost'], data['overtime_hour'])]) + overtime_cost_expr

# Complete objective function
problem += profit - cost_machines - c1_expr, "Total_Profit"

# Constraints
# Machine Time Constraints
for m in range(len(data['availability'])):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m], f"Machine_{m+1}_Time_Constraint"

# Minimum Batch Production
for p in range(P):
    problem += x[p] >= data['min_batches'][p], f"Min_Batch_Production_{p+1}"

# Profit Constraint
problem += profit - cost_machines - c1_expr >= data['min_profit'], "Profit_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')