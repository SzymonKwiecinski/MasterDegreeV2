import pulp

# Given data
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
    'dependencies': [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
}

M = len(data['buy_price'])
I = len(data['buy_price'][0])

# Initialize problem
problem = pulp.LpProblem("Oil_Supply_Problem", pulp.LpMaximize)

# Decision variables
buy = pulp.LpVariable.dicts("Buy", (range(M), range(I)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", (range(M), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(M+1), range(I)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("Use", (range(M), range(I)), cat='Binary')

# Initial storage constraint
for i in range(I):
    problem += storage[0][i] == data['init_amount']

# Storage constraint at the last month (End storage)
for i in range(I):
    problem += storage[M][i] == data['init_amount']

# Main constraints for each month
for m in range(M):
    # Storage balance constraints
    for i in range(I):
        problem += storage[m+1][i] == storage[m][i] + buy[m][i] - refine[m][i]
        problem += storage[m+1][i] <= data['storage_size']

    # Refining capacity constraints
    problem += pulp.lpSum(refine[m][i] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[m][i] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

    # Hardness constraints
    weighted_hardness = pulp.lpSum(data['hardness'][i] * refine[m][i] for i in range(I))
    total_refined = pulp.lpSum(refine[m][i] for i in range(I))
    problem += weighted_hardness >= data['min_hardness'] * total_refined
    problem += weighted_hardness <= data['max_hardness'] * total_refined

    # At most 3 oils can be used
    problem += pulp.lpSum(use[m][i] for i in range(I)) <= 3

    # Minimum usage if an oil is used
    for i in range(I):
        problem += refine[m][i] >= data['min_usage'] * use[m][i]

    # Dependency constraints
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += use[m][i] <= use[m][j]

# Objective function
revenue = pulp.lpSum(data['sell_price'] * pulp.lpSum(refine[m][i] for i in range(I)) for m in range(M))
purchase_cost = pulp.lpSum(data['buy_price'][m][i] * buy[m][i] for m in range(M) for i in range(I))
storage_cost = pulp.lpSum(data['storage_cost'] * storage[m][i] for m in range(1, M+1) for i in range(I))

problem += revenue - purchase_cost - storage_cost

# Solve the problem
problem.solve()

# Prepare output
output = {
    "buy": [[pulp.value(buy[m][i]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[m][i]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[m][i]) for i in range(I)] for m in range(M+1)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')