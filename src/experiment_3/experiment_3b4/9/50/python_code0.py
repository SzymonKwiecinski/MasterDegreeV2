import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

machines = range(len(data['machine_costs']))
parts = range(len(data['prices']))

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("Batches", parts, lowBound=0, cat='Continuous')
e = pulp.LpVariable.dicts("Extra_Time", machines, lowBound=0, cat='Continuous')

# Objective Function
profit_term = pulp.lpSum([data['prices'][p] * x[p] for p in parts])
cost_term = pulp.lpSum([data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in parts) + data['extra_costs'][m] * e[m] for m in machines])

problem += profit_term - cost_term

# Constraints
# Minimum Production Requirements
for p in parts:
    problem += x[p] >= data['min_batches'][p], f"Min_Batches_{p}"

# Machine Time Constraints
for m in machines:
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in parts) <= data['availability'][m] + e[m], f"Time_Constraint_{m}"

# Extra Time Constraints
for m in machines:
    problem += e[m] <= data['max_extra'][m], f"Max_Extra_Time_{m}"

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')