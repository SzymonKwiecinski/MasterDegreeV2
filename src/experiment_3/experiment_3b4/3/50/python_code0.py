import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Variables
P = len(data['prices'])
M = len(data['machine_costs'])

# Initialize the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=data['min_batches'][p]) for p in range(P)]
e = [pulp.LpVariable(f'e_{m}', lowBound=0, upBound=data['max_extra'][m]) for m in range(M)]

# Objective function
profit = sum(data['prices'][p] * x[p] for p in range(P))
machine_costs = sum(data['machine_costs'][m] * sum(data['time_required'][m][p] * x[p] for p in range(P)) for m in range(M))
extra_costs = sum(data['extra_costs'][m] * e[m] for m in range(M))

problem += profit - machine_costs - extra_costs

# Constraints
for m in range(M):
    problem += sum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')