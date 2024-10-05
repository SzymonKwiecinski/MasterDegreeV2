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

# Create the problem
problem = pulp.LpProblem("MaximizeProfit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(len(data['prices']))]
y = pulp.LpVariable('y', lowBound=0, cat='Continuous')
z = pulp.LpVariable('z', cat='Continuous')

# Objective function
profit = pulp.lpSum(
    data['prices'][p] * x[p] - pulp.lpSum(data['time_required'][m][p] * x[p] * data['machine_costs'][m] for m in range(1, len(data['machine_costs'])))
    for p in range(len(data['prices']))
) - (data['standard_cost'] * y + data['overtime_cost'] * z)

problem += profit

# Constraints
for m in range(1, len(data['availability'])):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(len(data['prices']))) <= data['availability'][m]

problem += y + z == pulp.lpSum(data['time_required'][0][p] * x[p] for p in range(len(data['prices'])))
problem += y <= data['overtime_hour']
problem += profit >= data['min_profit']

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')