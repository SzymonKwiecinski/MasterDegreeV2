import pulp
import numpy as np

# Data input
data = {'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'sell_price': 150, 'is_vegetable': [True, True, False, False, False], 'max_vegetable_refining_per_month': 200, 'max_non_vegetable_refining_per_month': 250, 'storage_size': 1000, 'storage_cost': 5, 'min_hardness': 3, 'max_hardness': 6, 'hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'init_amount': 500, 'min_usage': 20, 'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}

# Constants
M = len(data['buy_price'])  # Number of months
I = len(data['buy_price'][0])  # Number of oils
sell_price = data['sell_price']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
min_hardness = data['min_hardness']
max_hardness = data['max_hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
dependencies = np.array(data['dependencies'])
is_vegetable = data['is_vegetable']
hardness = data['hardness']
prices = np.array(data['buy_price'])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
buy = pulp.LpVariable.dicts("Buy", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((m, i) for m in range(M+1) for i in range(I)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("Use", ((m, i) for m in range(M) for i in range(I)), cat='Binary')

# Initial storage constraints
for i in range(I):
    problem += storage[0, i] == init_amount

# Storage constraints
for m in range(M):
    for i in range(I):
        problem += (storage[m+1, i] == storage[m, i] + buy[m, i] - refine[m, i])
        problem += (storage[m+1, i] <= storage_size)

# Production capacity constraints
for m in range(M):
    problem += pulp.lpSum(refine[m, i] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[m, i] for i in range(I) if not is_vegetable[i]) <= max_non_veg

# Hardness constraints
for m in range(M):
    hardness_product = pulp.lpSum(hardness[i] * refine[m, i] for i in range(I))
    total_refine = pulp.lpSum(refine[m, i] for i in range(I))
    problem += hardness_product >= min_hardness * total_refine
    problem += hardness_product <= max_hardness * total_refine

# Final product composition constraints
for m in range(M):
    for i in range(I):
        problem += refine[m, i] >= min_usage * use[m, i]  # Minimum usage
    problem += pulp.lpSum(use[m, i] for i in range(I)) <= 3  # Max 3 oils used

# Dependency constraints
for m in range(M):
    for i in range(I):
        for j in range(I):
            if dependencies[i, j]:
                problem += use[m, i] <= use[m, j]

# End storage constraints
for i in range(I):
    problem += storage[M, i] == init_amount

# Objective function
profit = pulp.lpSum((sell_price - prices[m][i]) * refine[m, i] - storage_cost * storage[m+1, i]
                    for m in range(M) for i in range(I))
problem += profit

# Solve the problem
problem.solve()

# Prepare the output
buy_solution = [[pulp.value(buy[m, i]) for i in range(I)] for m in range(M)]
refine_solution = [[pulp.value(refine[m, i]) for i in range(I)] for m in range(M)]
storage_solution = [[pulp.value(storage[m, i]) for i in range(I)] for m in range(M+1)]  # Including initial storage

output = {
    "buy": buy_solution,
    "refine": refine_solution,
    "storage": storage_solution
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')