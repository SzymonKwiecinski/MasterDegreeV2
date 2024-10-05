import pulp

# Parse the input data
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

# Extracting relevant data
I = len(data['buy_price'][0]) 
M = len(data['buy_price']) 
sell_price = data['sell_price']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
min_hardness = data['min_hardness']
max_hardness = data['max_hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M + 1)), lowBound=0, cat='Continuous')  # including month 0
use_oil = pulp.LpVariable.dicts("use_oil", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

# Initial storage
for i in range(I):
    problem += storage[(i, 0)] == init_amount  # Initial storage in month 0

# Storage constraints
for i in range(I):
    for m in range(M):
        problem += storage[(i, m + 1)] == storage[(i, m)] + buyquantity[(i, m)] - refine[(i, m)]
        problem += storage[(i, m + 1)] <= storage_size

# Refining capacity constraints
for m in range(M):
    problem += pulp.lpSum(refine[(i, m)] for i in range(I) if data['is_vegetable'][i]) <= max_veg
    problem += pulp.lpSum(refine[(i, m)] for i in range(I) if not data['is_vegetable'][i]) <= max_non_veg

# Hardness constraint
for m in range(M):
    hardness = pulp.lpSum(refine[(i, m)] * data['hardness'][i] for i in range(I))
    product_amount = pulp.lpSum(refine[(i, m)] for i in range(I))
    problem += (product_amount * min_hardness) <= hardness
    problem += hardness <= (product_amount * max_hardness)

# Usage constraints
for m in range(M):
    for i in range(I):
        problem += refine[(i, m)] >= min_usage * use_oil[(i, m)]
        problem += refine[(i, m)] <= storage[(i, m)] + buyquantity[(i, m)]

    # Limiting to three oils per month
    problem += pulp.lpSum(use_oil[(i, m)] for i in range(I)) <= 3

    # Dependency constraints
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += use_oil[(i, m)] <= use_oil[(j, m)]

# Ensure storage at the end is initial amount
for i in range(I):
    problem += storage[(i, M)] == init_amount

# Objective function
profit = (
    pulp.lpSum(refine[(i, m)] * sell_price for i in range(I) for m in range(M))
    - pulp.lpSum(buyquantity[(i, m)] * data['buy_price'][m][i] for i in range(I) for m in range(M))
    - pulp.lpSum(storage[(i, m)] * storage_cost for i in range(I) for m in range(M + 1))
)
problem += profit

# Solve the problem
problem.solve()

# Create output format
output = {
    "buy": [[pulp.value(buyquantity[(i, m)]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[(i, m)]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[(i, m)]) for i in range(I)] for m in range(M+1)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')