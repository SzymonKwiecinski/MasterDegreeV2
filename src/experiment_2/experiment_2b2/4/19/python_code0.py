import pulp

# Given data
data = {
    "buy_price": [
        [110, 120, 130, 110, 115],
        [130, 130, 110, 90, 115],
        [110, 140, 130, 100, 95],
        [120, 110, 120, 120, 125],
        [100, 120, 150, 110, 105],
        [90, 100, 140, 80, 135],
    ],
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
    "dependencies": [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
}

# Constants
I = len(data['buy_price'][0])  # Number of oils
M = len(data['buy_price'])     # Number of months

# Create problem
problem = pulp.LpProblem("Oil_Blend_Optimization", pulp.LpMaximize)

# Decision variables
buy = pulp.LpVariable.dicts("buy", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
use_indicator = pulp.LpVariable.dicts("use_indicator", ((m, i) for m in range(M) for i in range(I)), 0, 1, cat='Binary')

# Objective function: Maximize profit
revenue = pulp.lpSum(refine[m, i] * data['sell_price'] for m in range(M) for i in range(I))
purchase_cost = pulp.lpSum(buy[m, i] * data['buy_price'][m][i] for m in range(M) for i in range(I))
storage_cost = pulp.lpSum(storage[m, i] * data['storage_cost'] for m in range(M) for i in range(I))
problem += revenue - (purchase_cost + storage_cost)

# Constraints

# Storage balance
for m in range(M):
    for i in range(I):
        if m == 0:
            problem += storage[m, i] == data['init_amount'] + buy[m, i] - refine[m, i]
        else:
            problem += storage[m, i] == storage[m-1, i] + buy[m, i] - refine[m, i]

# Storage limits
for m in range(M):
    for i in range(I):
        problem += storage[m, i] <= data['storage_size']

# Refining limits
for m in range(M):
    problem += pulp.lpSum(refine[m, i] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[m, i] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Hardness constraint
for m in range(M):
    hardness_value = pulp.lpSum(refine[m, i] * data['hardness'][i] for i in range(I))
    refine_sum = pulp.lpSum(refine[m, i] for i in range(I))
    problem += hardness_value >= data['min_hardness'] * refine_sum
    problem += hardness_value <= data['max_hardness'] * refine_sum

# Exactly same storage at the end of last month
for i in range(I):
    problem += storage[M-1, i] == data['init_amount']

# No more than three oils in any month
for m in range(M):
    problem += pulp.lpSum(use_indicator[m, i] for i in range(I)) <= 3

# Minimum usage if used
for m in range(M):
    for i in range(I):
        problem += refine[m, i] >= data['min_usage'] * use_indicator[m, i]

# Dependency constraints
for m in range(M):
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += use_indicator[m, j] >= use_indicator[m, i]

# Solve the problem
problem.solve()

# Extract solution
buy_solution = [[pulp.value(buy[m, i]) for i in range(I)] for m in range(M)]
refine_solution = [[pulp.value(refine[m, i]) for i in range(I)] for m in range(M)]
storage_solution = [[pulp.value(storage[m, i]) for i in range(I)] for m in range(M)]

# Output
output = {
    "buy": buy_solution,
    "refine": refine_solution,
    "storage": storage_solution
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')