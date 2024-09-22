import pulp

# Data from JSON
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Parameters
C = data['capacity']
H = data['holding_cost']
P = data['price']
C_cost = data['cost']
N = len(P)

# Problem
problem = pulp.LpProblem("Warehouse_Operations_Optimization", pulp.LpMaximize)

# Variables
b = [pulp.LpVariable(f'b_{n}', lowBound=0) for n in range(N)]
s = [pulp.LpVariable(f's_{n}', lowBound=0) for n in range(N)]
x = [pulp.LpVariable(f'x_{n}', lowBound=0) for n in range(N)]

# Objective
problem += pulp.lpSum(P[n] * s[n] - C_cost[n] * b[n] - H * x[n] for n in range(N))

# Constraints

# Initial stock
problem += x[0] == 0 + b[0] - s[0]

# Stock dynamics and other constraints
for n in range(1, N):
    problem += x[n] == x[n-1] + b[n] - s[n]

# Capacity constraints
for n in range(N):
    problem += x[n] <= C

# Final stock constraint
problem += x[N-1] == 0

# Solve the problem
problem.solve()

print(f'Objective Value: <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output results
for n in range(N):
    print(f'Period {n+1}: Buy = {b[n].varValue}, Sell = {s[n].varValue}, Stock = {x[n].varValue}')