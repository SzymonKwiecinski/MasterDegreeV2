import pulp

# Data
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

# Indices
P = len(data['prices'])
M = len(data['machine_costs'])

# Decision Variables
x = pulp.LpVariable.dicts("Batch", range(P), lowBound=0, cat='Continuous')

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit_terms = [data['prices'][p] * x[p] for p in range(P)]
machine_cost_terms = [data['machine_costs'][m] * sum(data['time_required'][m][p] * x[p] for p in range(P)) for m in range(M)]
labor_cost_expr = sum(data['time_required'][0][p] * x[p] for p in range(P))
labor_cost = pulp.lpSum(data['standard_cost'] * labor_cost_expr)
overtime = labor_cost_expr - data['overtime_hour']
overtime_cost_expr = pulp.lpSum(data['overtime_cost'] * overtime) if overtime > 0 else 0
labor_cost += overtime_cost_expr
objective = pulp.lpSum(profit_terms) - pulp.lpSum(machine_cost_terms) - labor_cost

problem += objective

# Constraints
# Machine Availability constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m]

# Minimum Batch Requirement
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

# Minimum Profit Requirement
problem += objective >= data['min_profit']

# Solve
problem.solve()

# Print Objective
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')