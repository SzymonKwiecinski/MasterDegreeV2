import pulp
import numpy as np

# Data from JSON
data = {
    'buy_price': [[110, 120, 130, 110, 115], 
                  [130, 130, 110, 90, 115], 
                  [110, 140, 130, 100, 95], 
                  [120, 110, 120, 120, 125], 
                  [100, 120, 150, 110, 105], 
                  [90, 100, 140, 80, 135]],
    'sell_price': 150,
    'is_vegetable': [True, True, False, False, False],
    'max_vegetable_refining_per_month': 200,
    'max_non_vegetable_refining_per_month': 250,
    'storage_size': 1000,
    'storage_cost': 5,
    'min_hardness': 3,
    'max_hardness': 6,
    'hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'init_amount': 500,
    'min_usage': 20,
    'dependencies': [[0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0]]
}

M = 5  # Number of months
I = len(data['buy_price'])  # Number of oils

# Define the problem
problem = pulp.LpProblem("Oil_Refining_Optimization", pulp.LpMaximize)

# Decision variables
y = pulp.LpVariable.dicts("y", (range(I), range(M)), lowBound=0, cat='Continuous')  # Amount sold
x = pulp.LpVariable.dicts("x", (range(I), range(M)), lowBound=0, cat='Continuous')  # Amount bought
s = pulp.LpVariable.dicts("s", (range(I), range(M + 1)), lowBound=0, upBound=data['storage_size'], cat='Continuous')  # Storage
z = pulp.LpVariable.dicts("z", (range(I), range(M)), cat='Binary')  # Usage indicator

# Objective function
profit = pulp.lpSum(data['sell_price'] * y[i][m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(data['buy_price'][i][m] * x[i][m] for i in range(I) for m in range(M)) \
         - data['storage_cost'] * pulp.lpSum(s[i][m] for i in range(I) for m in range(M))

problem += profit

# Initial storage
for i in range(I):
    problem += s[i][0] == data['init_amount']

# Storage dynamics
for i in range(I):
    for m in range(1, M + 1):
        problem += s[i][m] == s[i][m - 1] + x[i][m - 1] - y[i][m - 1]

# Storage capacity
for i in range(I):
    for m in range(M + 1):
        problem += s[i][m] <= data['storage_size']

# Refining constraints
for m in range(M):
    problem += pulp.lpSum(y[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(y[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Hardness constraints
for m in range(M):
    problem += data['min_hardness'] <= pulp.lpSum(data['hardness'][i] * y[i][m] for i in range(I)) / pulp.lpSum(y[i][m] for i in range(I))
    problem += pulp.lpSum(data['hardness'][i] * y[i][m] for i in range(I)) / pulp.lpSum(y[i][m] for i in range(I)) <= data['max_hardness']
  
    problem += pulp.lpSum(y[i][m] for i in range(I)) >= data['min_usage'] * pulp.lpSum(z[i][m] for i in range(I))

# Oil usage constraints
for m in range(M):
    for i in range(I):
        problem += z[i][m] <= 1
        problem += y[i][m] <= z[i][m] * data['max_vegetable_refining_per_month'] if data['is_vegetable'][i] else y[i][m] <= z[i][m] * data['max_non_vegetable_refining_per_month']

        for j in range(I):
            problem += z[i][m] + z[j][m] >= data['dependencies'][i][j] * z[i][m]

    problem += pulp.lpSum(z[i][m] for i in range(I)) <= 3

# End of the last month storage
for i in range(I):
    problem += s[i][M] == data['init_amount']

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')