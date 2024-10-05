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

P = len(data['prices'])
M = len(data['availability'])

# Problem
problem = pulp.LpProblem("MaximizeProfit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x{p}', lowBound=0, cat='Integer') for p in range(P)]

# Objective Function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P))

standard_cost_machine_1 = pulp.lpSum(data['time_required'][0][p] * x[p] for p in range(P))
overtime_cost = (standard_cost_machine_1 - data['overtime_hour'])
overtime_cost_expr = pulp.lpSum([overtime_cost if overtime_cost > 0 else 0])

labor_cost_machine_1 = (
    data['standard_cost'] * standard_cost_machine_1 
    + data['overtime_cost'] * overtime_cost_expr
)

other_machines_cost = pulp.lpSum(
    data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) 
    for m in range(1, M)
)

total_cost = labor_cost_machine_1 + other_machines_cost

problem += profit - total_cost

# Constraints
# Machine Usage Constraints (for m = 2,...,M)
for m in range(1, M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m]

# Minimum Batches Requirement
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

# Profit Requirement
problem += (profit - total_cost) >= data['min_profit']

# Solve the problem
problem.solve()

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')