import pulp
import json

# Input data
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

# Problem setup
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
M = len(data['buy_price'])
I = len(data['buy_price'][0])
buyquantity = pulp.LpVariable.dicts("BuyQuantity", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(I), range(M+1)), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum([(data['sell_price'] * pulp.lpSum(refine[i][m] for i in range(I))) - 
                      pulp.lpSum(data['buy_price'][m][i] * buyquantity[i][m] for i in range(I))) for m in range(M)])

problem += profit

# Constraints

# Initial storage
for i in range(I):
    storage[i][0] = data['init_amount']

# Monthly storage constraint
for m in range(M):
    for i in range(I):
        problem += storage[i][m+1] == storage[i][m] + buyquantity[i][m] - refine[i][m]

# Storage capacity constraint
for i in range(I):
    for m in range(M+1):
        problem += storage[i][m] <= data['storage_size']

# Vegetable and non-vegetable refining limits
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Hardness constraints
for m in range(M):
    hardness_expr = pulp.lpSum(refine[i][m] * data['hardness'][i] for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I)) if pulp.lpSum(refine[i][m] for i in range(I)) > 0 else 1
    problem += hardness_expr >= data['min_hardness']
    problem += hardness_expr <= data['max_hardness']

# Dependency constraints
for m in range(M):
    for i in range(I):
        if data['dependencies'][i].count(1) > 0:
            problem += refine[i][m] <= pulp.lpSum(refine[j][m] for j in range(I) if data['dependencies'][i][j] == 1) * 100

# Minimum usage
for m in range(M):
    for i in range(I):
        problem += refine[i][m] <= (pulp.lpSum(refine[j][m] for j in range(I) if data['dependencies'][i][j] == 1) + 1) * 100
        problem += refine[i][m] >= data['min_usage']

# Final storage equals initial
for i in range(I):
    problem += storage[i][M] == data['init_amount']

# Solve the problem
problem.solve()

# Output results
buy_result = [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)]
refine_result = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_result = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M+1)]

output = {
    "buy": buy_result,
    "refine": refine_result,
    "storage": storage_result
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')