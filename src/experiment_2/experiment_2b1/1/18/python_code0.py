import pulp
import json

# Input data
data = {
    'M': 6,
    'I': 5,
    'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115],
                 [110, 140, 130, 100, 95], [120, 110, 120, 120, 125],
                 [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'SellPrice': 150,
    'IsVegetable': [True, True, False, False, False],
    'MaxVegetableRefiningPerMonth': 200,
    'MaxNonVegetableRefiningPerMonth': 250,
    'StorageSize': 1000,
    'StorageCost': 5,
    'MinHardness': 3,
    'MaxHardness': 6,
    'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'InitialAmount': 500
}

# Problem parameters
M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_veg = data['MaxVegetableRefiningPerMonth']
max_non_veg = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(sell_price * pulp.lpSum(refine[i, m] for i in range(I) for m in range(M)) - 
                      pulp.lpSum(buy_price[m][i] * buyquantity[i, m] for i in range(I) for m in range(M)) - 
                      storage_cost * pulp.lpSum(storage[i, m] for i in range(I) for m in range(M))), "Total Profit"

# Constraints
# Storage constraint for each oil
for i in range(I):
    for m in range(M):
        if m == 0:
            problem += storage[i, m] == init_amount + buyquantity[i, m] - refine[i, m], f"Storage_initial_{i}_{m}"
        else:
            problem += storage[i, m] == storage[i, m - 1] + buyquantity[i, m] - refine[i, m], f"Storage_{i}_{m}"

# Maximum storage constraint
for i in range(I):
    for m in range(M):
        problem += storage[i, m] <= storage_size, f"Storage_limit_{i}_{m}"

# Refining capacity constraints
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_veg, f"MaxVegRefining_{m}"
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_veg, f"MaxNonVegRefining_{m}"

# Hardness constraints
for m in range(M):
    problem += (pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / 
                 (pulp.lpSum(refine[i, m] for i in range(I)) + 1e-9)) >= min_hardness, f"MinHardness_{m}")
    problem += (pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / 
                 (pulp.lpSum(refine[i, m] for i in range(I)) + 1e-9)) <= max_hardness, f"MaxHardness_{m}")

# Last month's storage must equal initial amount
for i in range(I):
    problem += storage[i, M-1] == init_amount, f"FinalStorage_{i}"

# Solve the problem
problem.solve()

# Prepare output
buy = [[buyquantity[i, m].varValue for i in range(I)] for m in range(M)]
refine_res = [[refine[i, m].varValue for i in range(I)] for m in range(M)]
storage_res = [[storage[i, m].varValue for i in range(I)] for m in range(M)]

# Output result
result = {
    "buy": buy,
    "refine": refine_res,
    "storage": storage_res
}

print(json.dumps(result, indent=4))

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')