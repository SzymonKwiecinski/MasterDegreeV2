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

# Variables
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Initialize the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{p+1}", lowBound=0, cat='Continuous') for p in range(P)]
y = [pulp.LpVariable(f"y_{m+1}", lowBound=0, cat='Continuous') for m in range(M)]

# Objective function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P))
machine_costs = pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) + y[m]) for m in range(M))
extra_costs = pulp.lpSum(data['extra_costs'][m] * y[m] for m in range(M))

problem += profit - machine_costs - extra_costs

# Constraints
# Time availability constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) + y[m] <= data['availability'][m] + data['max_extra'][m]

# Minimum production requirements
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

# Extra time limit constraints
for m in range(M):
    problem += y[m] <= data['max_extra'][m]

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')