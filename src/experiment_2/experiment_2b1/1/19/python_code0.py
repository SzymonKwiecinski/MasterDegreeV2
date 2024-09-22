import pulp
import numpy as np
import json

data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], 
                  [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

I = len(data['buy_price'][0])
M = len(data['buy_price'])
sell_price = data['sell_price']
buy_price = np.array(data['buy_price'])
is_vegetable = np.array(data['is_vegetable'])
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
max_hardness = data['max_hardness']
min_hardness = data['min_hardness']
hardness = np.array(data['hardness'])
init_amount = data['init_amount']
min_usage = data['min_usage']
dependencies = np.array(data['dependencies'])

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("Buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in range(I) for m in range(M)) 
                    - pulp.lpSum(buy_price[m][i] * buyquantity[i][m] for i in range(I) for m in range(M)) 
                    - storage_cost * pulp.lpSum(storage[i][m] for i in range(I) for m in range(M)))
problem += profit

# Constraints
# Storage constraints
for i in range(I):
    for m in range(M):
        problem += storage[i][m] == init_amount + pulp.lpSum(buyquantity[i_prime][m] for i_prime in range(I) if i_prime != i) \
                                                 - pulp.lpSum(refine[i][m_prime] for m_prime in range(m+1)) \
                                                 + (storage[i][m-1] if m > 0 else init_amount)

# Refining limits
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_veg

# Hardness constraints
for m in range(M):
    problem += pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I)) >= min_hardness
    problem += pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I)) <= max_hardness

# Dependency constraints
for m in range(M):
    for i in range(I):
        if dependencies[i].sum() > 0:
            problem += refine[i][m] <= pulp.lpSum(refine[j][m] for j in range(I) if dependencies[j][i] == 1) * 10000

# Minimum usage constraints
for m in range(M):
    for i in range(I):
        problem += refine[i][m] >= min_usage

# Solve the problem
problem.solve()

# Output results
results = {
    "buy": [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps(results))