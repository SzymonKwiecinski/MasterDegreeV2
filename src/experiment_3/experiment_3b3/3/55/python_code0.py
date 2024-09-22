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

# Number of parts and machines
P = len(data['prices'])
M = len(data['machine_costs'])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
batches = [pulp.LpVariable(f'b_{p}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]

# Objective Function

# Labor Cost Calculation
labor_cost_expr = (
    pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P))
)
labor_cost = (data['standard_cost'] * data['overtime_hour'] +
              data['overtime_cost'] * (labor_cost_expr - data['overtime_hour']))

# Total Cost
total_machine_cost = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(1, M))
total_revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))

# Profit Objective
problem += total_revenue - total_machine_cost - labor_cost, "Total_Profit"

# Constraints

# Machine availability constraints
for m in range(1, M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], f'Machine_{m}_availability'

# Minimum production requirement for each part
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f'Min_batches_{p}'

# Profit constraint
problem += total_revenue - total_machine_cost - labor_cost >= data['min_profit'], "Minimum_Profit"

# Solve
problem.solve()

# Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')