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

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
P = len(data['prices'])
x = [pulp.LpVariable(f'x_{p+1}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]

# Objective Function
# Calculate Cost for Machine 1
time_machine_1 = sum(data['time_required'][0][p] * x[p] for p in range(P))
Cost_Machine_1 = pulp.LpVariable('Cost_Machine_1', lowBound=0, cat='Continuous')

problem += Cost_Machine_1 == pulp.lpSum([
    time_machine_1 * data['standard_cost'],
    (time_machine_1 - data['overtime_hour']) * (data['overtime_cost'] - data['standard_cost']) * (time_machine_1 > data['overtime_hour'])
])

# Objective Function
profits = pulp.lpSum(data['prices'][p] * x[p] for p in range(P))
costs = pulp.lpSum(data['machine_costs'][m] * sum(data['time_required'][m][p] * x[p] for p in range(P)) for m in range(1, len(data['machine_costs'])))
problem += profits - costs - Cost_Machine_1

# Constraints
# Machine time constraints (excluding machine 1)
for m in range(1, len(data['availability'])):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m]

# Minimum profit constraint
problem += profits - costs - Cost_Machine_1 >= data['min_profit']

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')