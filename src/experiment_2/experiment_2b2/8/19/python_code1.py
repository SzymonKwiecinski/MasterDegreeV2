import pulp

# Data
data = {
    "buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    "sell_price": 150,
    "is_vegetable": [True, True, False, False, False],
    "max_vegetable_refining_per_month": 200,
    "max_non_vegetable_refining_per_month": 250,
    "storage_size": 1000,
    "storage_cost": 5,
    "min_hardness": 3,
    "max_hardness": 6,
    "hardness": [8.8, 6.1, 2.0, 4.2, 5.0],
    "init_amount": 500,
    "min_usage": 20,
    "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

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

I = len(buy_price[0])
M = len(buy_price)

# Define the problem
problem = pulp.LpProblem("Food_Manufacturing", pulp.LpMaximize)

# Decision variables
buy = pulp.LpVariable.dicts("buy", ((m, i) for m in range(M) for i in range(I)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((m, i) for m in range(M) for i in range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((m, i) for m in range(M + 1) for i in range(I)), lowBound=0)

# Initial storage constraint
for i in range(I):
    problem += storage[0, i] == init_amount

# Objective: Maximize profit
profit = pulp.lpSum(
    (sell_price * pulp.lpSum(refine[m, i] for i in range(I))) -
    (pulp.lpSum(buy_price[m][i] * buy[m, i] for i in range(I))) -
    (storage_cost * pulp.lpSum(storage[m, i] for i in range(I)))
    for m in range(M)
)

problem += profit

# Constraints
for m in range(M):
    veg_refining = pulp.lpSum(refine[m, i] for i in range(I) if is_vegetable[i])
    non_veg_refining = pulp.lpSum(refine[m, i] for i in range(I) if not is_vegetable[i])

    problem += veg_refining <= max_veg
    problem += non_veg_refining <= max_non_veg

    for i in range(I):
        # Storage balance constraints
        problem += storage[m + 1, i] == storage[m, i] + buy[m, i] - refine[m, i]

        # Storage capacity constraints
        problem += storage[m + 1, i] <= storage_size

    # Hardness constraints
    hardness_expr = pulp.lpSum(refine[m, i] * hardness[i] for i in range(I))
    total_refine = pulp.lpSum(refine[m, i] for i in range(I))
    
    if total_refine > 0:  # Avoid division by zero
        problem += hardness_expr <= max_hardness * total_refine
        problem += hardness_expr >= min_hardness * total_refine

    # Only use up to 3 oils constraint
    problem += pulp.lpSum(pulp.lpSum(refine[m, i] >= min_usage for i in range(I))) <= 3

    # Dependency constraints
    for i in range(I):
        for j in range(I):
            if dependencies[i][j] == 1:
                problem += refine[m, i] >= min_usage * (refine[m, j] / max_veg if is_vegetable[j] else refine[m, j] / max_non_veg)

# Final storage constraint
for i in range(I):
    problem += storage[M, i] == init_amount

# Solve the problem
problem.solve()

# Output the results
output = {
    "buy": [[pulp.value(buy[m, i]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[m, i]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[m, i]) for i in range(I)] for m in range(M + 1)]
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')