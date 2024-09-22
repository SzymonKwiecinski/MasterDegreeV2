import pulp

# Input data
data = {
    'M': 6, 
    'I': 5, 
    'BuyPrice': [
        [110, 120, 130, 110, 115], 
        [130, 130, 110, 90, 115], 
        [110, 140, 130, 100, 95], 
        [120, 110, 120, 120, 125], 
        [100, 120, 150, 110, 105], 
        [90, 100, 140, 80, 135]
    ], 
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

# Extracting data from the input
M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_veg_refining = data['MaxVegetableRefiningPerMonth']
max_non_veg_refining = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

# LP Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buy_quantity = pulp.LpVariable.dicts("BuyQty", ((m, i) for m in range(M) for i in range(I)), lowBound=0)
refine_quantity = pulp.LpVariable.dicts("RefineQty", ((m, i) for m in range(M) for i in range(I)), lowBound=0)
storage_quantity = pulp.LpVariable.dicts("StorageQty", ((m, i) for m in range(M+1) for i in range(I)), lowBound=0)

# Initial storage
for i in range(I):
    problem += storage_quantity[0, i] == init_amount

# Constraints
for m in range(M):
    # Refining constraints
    problem += pulp.lpSum(refine_quantity[(m, i)] for i in range(I) if is_vegetable[i]) <= max_veg_refining
    problem += pulp.lpSum(refine_quantity[(m, i)] for i in range(I) if not is_vegetable[i]) <= max_non_veg_refining

    # Storage constraints and flow balance
    for i in range(I):
        problem += (storage_quantity[(m, i)] + buy_quantity[(m, i)] == refine_quantity[(m, i)] + storage_quantity[(m+1, i)])
        problem += storage_quantity[(m+1, i)] <= storage_size

    # Hardness constraints
    total_refined = pulp.lpSum(refine_quantity[m, i] for i in range(I))
    if total_refined > 0:
        avg_hardness = pulp.lpSum(hardness[i] * refine_quantity[m, i] for i in range(I)) / total_refined
        problem += avg_hardness >= min_hardness
        problem += avg_hardness <= max_hardness

# Ending storage must match initial amount
for i in range(I):
    problem += storage_quantity[(M, i)] == init_amount

# Objective Function: Maximize profit
profit = pulp.lpSum(
    (sell_price * pulp.lpSum(refine_quantity[(m, i)] for i in range(I))) -
    (pulp.lpSum(buy_price[m][i] * buy_quantity[(m, i)] for i in range(I))) -
    (storage_cost * pulp.lpSum(storage_quantity[(m+1, i)] for i in range(I)))
    for m in range(M)
)

problem += profit

# Solve the problem
problem.solve()

# Extracting results
buy = [[pulp.value(buy_quantity[m, i]) for i in range(I)] for m in range(M)]
refine = [[pulp.value(refine_quantity[m, i]) for i in range(I)] for m in range(M)]
storage = [[pulp.value(storage_quantity[m, i]) for i in range(I)] for m in range(M+1)]

# Output
output = {
    "buy": buy,
    "refine": refine,
    "storage": storage
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')