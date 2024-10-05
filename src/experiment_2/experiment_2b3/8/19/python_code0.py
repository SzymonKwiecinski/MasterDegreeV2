import pulp

# Problem data
data = {
    'buy_price': [
        [110, 120, 130, 110, 115],
        [130, 130, 110, 90, 115],
        [110, 140, 130, 100, 95],
        [120, 110, 120, 120, 125],
        [100, 120, 150, 110, 105],
        [90, 100, 140, 80, 135]
    ],
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
    'dependencies': [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
}

# Extract the data input for easy access
buy_price = data['buy_price']
sell_price = data['sell_price']
is_vegetable = data['is_vegetable']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
min_hardness = data['min_hardness']
max_hardness = data['max_hardness']
hardness = data['hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
dependencies = data['dependencies']

M = len(buy_price)
I = len(buy_price[0])

# Define LP problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Decision variables
buy = pulp.LpVariable.dicts("Buy", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((m, i) for m in range(M + 1) for i in range(I)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("Use", ((m, i) for m in range(M) for i in range(I)), cat='Binary')

# Objective function: Maximize profit
storage_cost_total = pulp.lpSum(storage_cost * storage[m, i] for m in range(M) for i in range(I))
buy_cost_total = pulp.lpSum(buy_price[m][i] * buy[m, i] for m in range(M) for i in range(I))
sell_revenue_total = pulp.lpSum(sell_price * refine[m, i] for m in range(M) for i in range(I))

profit = sell_revenue_total - buy_cost_total - storage_cost_total
problem += profit

# Initial storage amounts
for i in range(I):
    problem += storage[0, i] == init_amount

# Constraints
for m in range(M):
    # Storage balance
    for i in range(I):
        problem += storage[m + 1, i] == storage[m, i] + buy[m, i] - refine[m, i]

    # Refining limits
    problem += pulp.lpSum(refine[m, i] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[m, i] for i in range(I) if not is_vegetable[i]) <= max_non_veg

    # Hardness constraints
    total_refine = pulp.lpSum(refine[m, i] for i in range(I))
    if total_refine > 0:
        hardness_average = pulp.lpSum(hardness[i] * refine[m, i] for i in range(I)) / total_refine
        problem += hardness_average >= min_hardness
        problem += hardness_average <= max_hardness

    # Minimum usage constraints
    for i in range(I):
        problem += refine[m, i] >= min_usage * use[m, i]
        problem += refine[m, i] <= storage[m, i] + buy[m, i]

    # Dependency constraints
    for i in range(I):
        for j in range(I):
            if dependencies[i][j] == 1:
                problem += use[m, i] <= use[m, j]

    # At most 3 oils can be used in a month
    problem += pulp.lpSum(use[m, i] for i in range(I)) <= 3

# Final storage requirement
for i in range(I):
    problem += storage[M, i] == init_amount

# Solve the problem
problem.solve()

# Extract solution
solution = {
    "buy": [[pulp.value(buy[m, i]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[m, i]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[m, i]) for i in range(I)] for m in range(M + 1)]
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')