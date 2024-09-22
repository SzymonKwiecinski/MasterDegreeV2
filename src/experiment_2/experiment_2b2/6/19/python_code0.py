import pulp

# Load data
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
    'max_hardness': 6,
    'min_hardness': 3,
    'hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'init_amount': 500,
    'min_usage': 20,
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

M = len(data['buy_price'])
I = len(data['buy_price'][0])

# Define problem
problem = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

# Variables
buy = pulp.LpVariable.dicts("Buy", ((m, i) for m in range(M) for i in range(I)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", ((m, i) for m in range(M) for i in range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((m, i) for m in range(M) for i in range(I)), lowBound=0, upBound=data['storage_size'])

use_oil = pulp.LpVariable.dicts("UseOil", ((m, i) for m in range(M) for i in range(I)), cat='Binary')

# Initial storage
for i in range(I):
    problem += storage[(0, i)] == data['init_amount']

# Constraints
for m in range(M):
    # Refining constraints
    problem += pulp.lpSum(refine[(m, i)] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[(m, i)] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

    # Storage balance constraints
    for i in range(I):
        problem += storage[(m, i)] == (storage[(m - 1, i)] if m > 0 else data['init_amount']
                                        - refine[(m, i)] + buy[(m, i)])

    # Hardness constraints
    problem += pulp.lpSum(refine[(m, i)] * data['hardness'][i] for i in range(I)) / pulp.lpSum(refine[(m, i)] for i in range(I)) <= data['max_hardness']
    problem += pulp.lpSum(refine[(m, i)] * data['hardness'][i] for i in range(I)) / pulp.lpSum(refine[(m, i)] for i in range(I)) >= data['min_hardness']

    # Usage constraints
    for i in range(I):
        problem += refine[(m, i)] >= use_oil[(m, i)] * data['min_usage']
        problem += refine[(m, i)] <= (storage[(m - 1, i)] if m > 0 else data['init_amount'])

    # Dependency constraints
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += use_oil[(m, i)] <= use_oil[(m, j)]

    # Max number of oils constraint
    problem += pulp.lpSum(use_oil[(m, i)] for i in range(I)) <= 3

# Final storage constraints
for i in range(I):
    problem += storage[(M - 1, i)] == data['init_amount']

# Objective function
profit = pulp.lpSum(refine[(m, i)] * data['sell_price'] for m in range(M) for i in range(I))
costs = pulp.lpSum(buy[(m, i)] * data['buy_price'][m][i] for m in range(M) for i in range(I)) + \
        pulp.lpSum(storage[(m, i)] * data['storage_cost'] for m in range(M) for i in range(I))

problem += profit - costs

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "buy": [[pulp.value(buy[(m, i)]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[(m, i)]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[(m, i)]) for i in range(I)] for m in range(M)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')