import pulp
import numpy as np

# Parse the input data
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

buy_price = data['buy_price']
sell_price = data['sell_price']
is_vegetable = data['is_vegetable']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
max_hardness = data['max_hardness']
min_hardness = data['min_hardness']
hardness = data['hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
dependencies = data['dependencies']

M = len(buy_price)
I = len(buy_price[0])
big_M = 1e6

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buy = pulp.LpVariable.dicts("buy", (range(M), range(I)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(M), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(M+1), range(I)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("use", (range(M), range(I)), cat='Binary')

# Objective function: Maximize profit
revenue = pulp.lpSum(sell_price * pulp.lpSum(refine[m][i] for i in range(I)) for m in range(M))
costs = pulp.lpSum(buy[m][i] * buy_price[m][i] + storage_cost * storage[m+1][i] for m in range(M) for i in range(I))
problem += revenue - costs

# Constraints
for m in range(M):
    for i in range(I):
        # Storage balance constraints
        if m == 0:
            problem += storage[m][i] == init_amount + buy[m][i] - refine[m][i]
        else:
            problem += storage[m][i] == storage[m-1][i] + buy[m][i] - refine[m][i]

        # Storage capacity constraints
        problem += storage[m][i] <= storage_size

        # Logic constraints using big-M method
        problem += refine[m][i] <= use[m][i] * big_M
        problem += refine[m][i] >= use[m][i] * min_usage

    # Hardness constraint
    hardness_constraint = pulp.lpSum(hardness[i] * refine[m][i] for i in range(I))
    total_refine = pulp.lpSum(refine[m][i] for i in range(I))
    problem += hardness_constraint >= min_hardness * total_refine
    problem += hardness_constraint <= max_hardness * total_refine

    # Refining capacity constraints
    problem += pulp.lpSum(refine[m][i] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[m][i] for i in range(I) if not is_vegetable[i]) <= max_non_veg

    # At most three oils used
    problem += pulp.lpSum(use[m][i] for i in range(I)) <= 3

    # Dependency constraints
    for i in range(I):
        for j in range(I):
            if dependencies[i][j]:
                problem += use[m][i] <= use[m][j]

# End-of-period storage constraint
for i in range(I):
    problem += storage[M][i] == init_amount

# Solve the problem
problem.solve()

# Retrieve results
buy_result = [[pulp.value(buy[m][i]) for i in range(I)] for m in range(M)]
refine_result = [[pulp.value(refine[m][i]) for i in range(I)] for m in range(M)]
storage_result = [[pulp.value(storage[m][i]) for i in range(I)] for m in range(M+1)]

output = {
    "buy": buy_result,
    "refine": refine_result,
    "storage": storage_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')