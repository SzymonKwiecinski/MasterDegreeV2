import pulp

# Data provided
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10], 
    'extra_costs': [0, 15, 22.5], 
    'max_extra': [0, 80, 80]
}

# Numbers of parts and machines
P = len(data['prices'])
M = len(data['machine_costs'])

# Decision Variables
x = [pulp.LpVariable(f"x_{p}", lowBound=data['min_batches'][p]) for p in range(P)]
e = [pulp.LpVariable(f"e_{m}", lowBound=0, upBound=data['max_extra'][m]) for m in range(M)]

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P))
machine_costs = pulp.lpSum(
    data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) + data['extra_costs'][m] * e[m]
    for m in range(M)
)
problem += profit - machine_costs

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m]

# Solve the problem
problem.solve()

# Print the objectives
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')