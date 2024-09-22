import pulp
import json

# Data input (simulating the given data as if it were read from a JSON file)
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

# Initializing the problem
M = len(data['buy_price'][0]) - 1  # Number of months
I = len(data['buy_price'])           # Number of oil types
problem = pulp.LpProblem("Oil_Refining_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M + 1)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M + 1)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M + 1)), lowBound=0, upBound=data['storage_size'])
use = pulp.LpVariable.dicts("use", ((i, m) for i in range(I) for m in range(M + 1)), cat=pulp.LpBinary)

# Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(M + 1)) - \
         pulp.lpSum((data['buy_price'][i][m] * buyquantity[i, m] + data['storage_cost'] * storage[i, m-1]) 
                     for i in range(I) for m in range(1, M + 1))

problem += profit

# Constraints
# Material Balance
for m in range(1, M + 1):
    for i in range(I):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]

# Initial Storage Constraint
for i in range(I):
    problem += storage[i, 0] == data['init_amount']

# Final Storage Constraint
for i in range(I):
    problem += storage[i, M] == data['init_amount']

# Capacity Constraints
for m in range(M + 1):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Storage Capacity Constraints
for m in range(M + 1):
    for i in range(I):
        problem += storage[i, m] <= data['storage_size']

# Hardness Constraint
for m in range(1, M + 1):
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) >= data['min_hardness']
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) <= data['max_hardness']

# Oil Usage Constraints
for m in range(M + 1):
    problem += pulp.lpSum(use[i, m] for i in range(I)) <= 3
    for i in range(I):
        problem += refine[i, m] >= data['min_usage'] * use[i, m]

# Dependency Constraints
for m in range(M + 1):
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += use[i, m] <= use[j, m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')