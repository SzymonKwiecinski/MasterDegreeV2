import pulp
import json

# Data input
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

# Parameters
I = len(data['buy_price'])  # Number of different oils
M = len(data['buy_price'][0])  # Number of months

# Create the problem
problem = pulp.LpProblem("Food_Manufacturing_Profit_Optimization", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0)

# Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(buyquantity[i, m] * data['buy_price'][i][m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(storage[i, m] * data['storage_cost'] for i in range(I) for m in range(M))
problem += profit

# Constraints
# Initial Storage
for i in range(I):
    problem += storage[i, 0] == data['init_amount'], f"Initial_Storage_{i}"

# Final Storage
for i in range(I):
    problem += storage[i, M] == data['init_amount'], f"Final_Storage_{i}"

# Storage Constraint
for m in range(1, M+1):
    for i in range(I):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m-1] - refine[i, m-1], f"Storage_Constraint_{i}_{m}"

# Refining Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month'], f"Vegetable_Capacity_{m}"
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month'], f"NonVegetable_Capacity_{m}"

# Hardness Constraints
for m in range(M):
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) / (pulp.lpSum(refine[i, m] for i in range(I)) + 1e-5) <= data['max_hardness'], f"Max_Hardness_{m}"
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) / (pulp.lpSum(refine[i, m] for i in range(I)) + 1e-5) >= data['min_hardness'], f"Min_Hardness_{m}"

# Oil Usage Constraints
for m in range(M):
    for i in range(I):
        problem += refine[i, m] >= data['min_usage'] * pulp.LpVariable(f'y_{i}_{m}', cat='Binary'), f"Min_Usage_{i}_{m}"

# Dependency Constraints
for m in range(M):
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += refine[j, m] >= data['min_usage'] * (pulp.LpVariable(f'y_{i}_{m}', cat='Binary') + pulp.LpVariable(f'y_{j}_{m}', cat='Binary') - 1), f"Dependency_{i}_{j}_{m}"

# Limit on the number of oils
for m in range(M):
    problem += pulp.lpSum(pulp.LpVariable(f'y_{i}_{m}', cat='Binary') for i in range(I)) <= 3, f"Oil_Limit_{m}"

# Solve problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')