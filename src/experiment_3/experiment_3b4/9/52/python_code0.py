import pulp

# Data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Sets
P = range(len(data['supply']))
C = range(len(data['demand']))

# Decision Variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in P for c in C), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p, c] for p in P for c in C)

# Constraints
# Supply constraints
for p in P:
    problem += pulp.lpSum(send[p, c] for c in C) <= data['supply'][p]

# Demand constraints
for c in C:
    problem += pulp.lpSum(send[p, c] for p in P) == data['demand'][c]

# Solve the problem
problem.solve()

# Print Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')