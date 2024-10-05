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
M = len(data['machine_costs'])

# Decision Variables
x = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Objective Function
total_time_1 = pulp.lpSum(data['time_required'][0][p] * x[p] for p in range(P))
labor_cost = (
    data['standard_cost'] * total_time_1
    if total_time_1 <= data['overtime_hour']
    else data['standard_cost'] * data['overtime_hour'] + data['overtime_cost'] * (total_time_1 - data['overtime_hour'])
)

total_profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P)) - pulp.lpSum(
    data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) for m in range(M)
) - labor_cost

problem += total_profit

# Constraints
# Machine availability
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m]

# Minimum batches
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

# Minimum profit
problem += total_profit >= data['min_profit']

# Solve
problem.solve()

# Output
for p in range(P):
    print(f'Batches produced for part {p+1}: {x[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')