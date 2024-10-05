import pulp

# Data
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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

M = len(data['buy_price'])  # number of months
I = len(data['buy_price'][0])  # number of oils

# Problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Variables
buy = pulp.LpVariable.dicts("buy", (range(M), range(I)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(M), range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(M+1), range(I)), lowBound=0)
use_indicator = pulp.LpVariable.dicts("use_indicator", (range(M), range(I)), cat='Binary')

# Objective
revenue = pulp.lpSum(refine[m][i] * data['sell_price'] for m in range(M) for i in range(I))
cost = pulp.lpSum(buy[m][i] * data['buy_price'][m][i] for m in range(M) for i in range(I))
storage_cost = pulp.lpSum(storage[m][i] * data['storage_cost'] for m in range(1, M+1) for i in range(I))
problem += revenue - cost - storage_cost

# Constraints
for i in range(I):
    # Initial storage
    problem += storage[0][i] == data['init_amount']
    # Final storage
    problem += storage[M][i] == data['init_amount']

for m in range(M):
    # Storage constraints
    for i in range(I):
        problem += storage[m+1][i] == storage[m][i] + buy[m][i] - refine[m][i]
        problem += storage[m+1][i] <= data['storage_size']

    # Refining constraints
    problem += pulp.lpSum(refine[m][i] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[m][i] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

    # Hardness constraints
    total_refine = pulp.lpSum(refine[m][i] for i in range(I))
    hardness_expression = pulp.lpSum(refine[m][i] * data['hardness'][i] for i in range(I))
    problem += total_refine * data['min_hardness'] <= hardness_expression
    problem += hardness_expression <= total_refine * data['max_hardness']

    # Oil usage constraints
    for i in range(I):
        problem += refine[m][i] >= data['min_usage'] * use_indicator[m][i]
        problem += refine[m][i] <= storage[m][i]

    # Maximum 3 oils condition
    problem += pulp.lpSum(use_indicator[m][i] for i in range(I)) <= 3

    # Dependencies
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += use_indicator[m][i] <= use_indicator[m][j]

# Solve
problem.solve()

# Output
output = {
    "buy": [[pulp.value(buy[m][i]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[m][i]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[m][i]) for i in range(I)] for m in range(M+1)]  # Including initial storage
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')