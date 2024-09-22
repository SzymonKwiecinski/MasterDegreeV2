import pulp
import numpy as np

# Data
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], 
                  [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], 
                  [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0]]
}

I = len(data['buy_price'])  # Number of oil types
M = len(data['buy_price'][0])  # Number of months

# Create the problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0)

# Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(M)) -\
         pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] for i in range(I) for m in range(M)) -\
         pulp.lpSum(data['storage_cost'] * storage[i, m] for i in range(I) for m in range(M))

problem += profit

# Constraints

# Production Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Storage Dynamics
for i in range(I):
    for m in range(1, M):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]

# Initial and Final Storage Constraints
for i in range(I):
    problem += storage[i, 0] == data['init_amount']
    problem += storage[i, M-1] == data['init_amount']

# Hardness Constraints
for m in range(M):
    problem += (pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) /
                pulp.lpSum(refine[i, m] for i in range(I))) >= data['min_hardness']
    problem += (pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) /
                pulp.lpSum(refine[i, m] for i in range(I))) <= data['max_hardness']

# Usage Constraints
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= data['min_usage'] * (1 if pulp.lpSum(refine[j, m] for j in range(I)) > 0 else 0)

# Dependency Constraints
for i in range(I):
    for j in range(I):
        if data['dependencies'][i][j] == 1:
            for m in range(M):
                problem += refine[i, m] <= refine[j, m]

# Oil Usage Limit
for m in range(M):
    problem += pulp.lpSum((1 if refine[i, m] > 0 else 0) for i in range(I)) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')