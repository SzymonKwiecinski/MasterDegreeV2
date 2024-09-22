import pulp
import json

# Data provided in JSON format
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], 
                  [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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

# Problem variables
I = len(data['buy_price'][0])  # Number of oils
M = len(data['buy_price'])  # Number of months

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum([(data['sell_price'] * pulp.lpSum(refine[i][m] for i in range(I))) - 
                        pulp.lpSum(data['buy_price'][m][i] * buyquantity[i][m] for i in range(I)) - 
                        data['storage_cost'] * storage[i][m] for m in range(M)]) 

# Constraints

# Storage initialization
for i in range(I):
    problem += storage[i][0] == data['init_amount'], f"InitStorageOil.{i}"

# Storage and refining constraints
for m in range(M):
    for i in range(I):
        # Storage balance
        if m > 0:
            problem += storage[i][m] == storage[i][m - 1] + buyquantity[i][m] - refine[i][m], f"StorageBalanceOil.{i}.{m}"
        else:
            problem += storage[i][m] == data['init_amount'] + buyquantity[i][m] - refine[i][m], f"StorageBalanceOil.{i}.{m}"

    # Refining constraints
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month'], f"MaxVegRefining.{m}"
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month'], f"MaxNonVegRefining.{m}"

# Hardness constraints
for m in range(M):
    problem += (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / 
                 pulp.lpSum(refine[i][m] for i in range(I)) >= data['min_hardness']), f"MinHardness.{m}"
    problem += (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / 
                 pulp.lpSum(refine[i][m] for i in range(I)) <= data['max_hardness']), f"MaxHardness.{m}"

# Minimum usage constraints
for m in range(M):
    for i in range(I):
        if data['min_usage'] > 0:
            problem += refine[i][m] >= data['min_usage'] * pulp.lpSum([1 for j in range(I) if data['dependencies'][i][j] == 1]), f"MinUsageOil.{i}.{m}"

# Last month storage constraint
for i in range(I):
    problem += storage[i][M-1] == data['init_amount'], f"FinalStorageOil.{i}"

# Solve the problem
problem.solve()

# Output results
buy = [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)]
refine_out = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_out = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]

result = {
    "buy": buy,
    "refine": refine_out,
    "storage": storage_out
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')