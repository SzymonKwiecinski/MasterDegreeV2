import pulp
import json

# Input data
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
    'min_hardness': 3,
    'max_hardness': 6,
    'hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'init_amount': 500,
    'min_usage': 20,
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0]]
}

# Parameters extraction
I = len(data['buy_price'][0])  # number of oils
M = len(data['buy_price'])  # number of months
buy_price = data['buy_price']
sell_price = data['sell_price']
is_vegetable = data['is_vegetable']
max_vegetable_refining_per_month = data['max_vegetable_refining_per_month']
max_non_vegetable_refining_per_month = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
min_hardness = data['min_hardness']
max_hardness = data['max_hardness']
hardness = data['hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
dependencies = data['dependencies']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum([sell_price * pulp.lpSum(refine[i][m] for m in range(M)) - 
                      pulp.lpSum(buy_price[m][i] * buyquantity[i][m] for m in range(M)) - 
                      pulp.lpSum(storage_cost * storage[i][m] for m in range(M)) 
                      for i in range(I)])
problem += profit

# Constraints
# Monthly refining limits
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_vegetable_refining_per_month
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_vegetable_refining_per_month

# Hardness constraints
for m in range(M):
    total_refined = pulp.lpSum(refine[j][m] for j in range(I))
    if total_refined > 0:
        hardness_expr = pulp.lpSum(hardness[i] * (refine[i][m] / total_refined) 
                                    for i in range(I) if refine[i][m] > 0)
        problem += hardness_expr >= min_hardness
        problem += hardness_expr <= max_hardness

# Storage constraints
for i in range(I):
    for m in range(M):
        if m == 0:
            problem += storage[i][m] == init_amount
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]
        problem += storage[i][m] <= storage_size

# Final month storage must equal initial amount
for i in range(I):
    problem += storage[i][M-1] == init_amount

# Use dependency constraints
for i in range(I):
    for m in range(M):
        if dependencies[i][-1] == 1:
            problem += refine[i][m] <= pulp.lpSum(refine[j][m] for j in range(I) if dependencies[j][i] == 1)

# Solve the problem
problem.solve()

# Output the results
buy_result = [[buyquantity[i][m].varValue for i in range(I)] for m in range(M)]
refine_result = [[refine[i][m].varValue for i in range(I)] for m in range(M)]
storage_result = [[storage[i][m].varValue for i in range(I)] for m in range(M)]

results = {
    "buy": buy_result,
    "refine": refine_result,
    "storage": storage_result
}

print(json.dumps(results, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')