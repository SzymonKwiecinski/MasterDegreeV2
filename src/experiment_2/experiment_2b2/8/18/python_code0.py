import pulp

# Data input
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

# Problem data
M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_v_refining = data['MaxVegetableRefiningPerMonth']
max_nv_refining = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

# LP Problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Variables
buy = pulp.LpVariable.dicts("Buy", (range(M), range(I)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", (range(M), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(M+1), range(I)), lowBound=0, upBound=storage_size, cat='Continuous')

# Initial storage
for i in range(I):
    problem += storage[0][i] == init_amount

# Constraints
for m in range(M):
    v_refining = pulp.lpSum(refine[m][i] for i in range(I) if is_vegetable[i])
    nv_refining = pulp.lpSum(refine[m][i] for i in range(I) if not is_vegetable[i])

    problem += v_refining <= max_v_refining
    problem += nv_refining <= max_nv_refining

    for i in range(I):
        problem += storage[m+1][i] == storage[m][i] + buy[m][i] - refine[m][i]
        
    hardness_constraint = pulp.lpSum((hardness[i] * refine[m][i]) for i in range(I))
    product_total = pulp.lpSum(refine[m][i] for i in range(I))
    
    problem += hardness_constraint <= max_hardness * product_total
    problem += hardness_constraint >= min_hardness * product_total

# End of month storage constraints
for i in range(I):
    problem += storage[M][i] == init_amount

# Objective Function
revenue = pulp.lpSum(sell_price * refine[m][i] for m in range(M) for i in range(I))
purchase_cost = pulp.lpSum(buy_price[m][i] * buy[m][i] for m in range(M) for i in range(I))
storage_cost_total = pulp.lpSum(storage_cost * storage[m+1][i] for m in range(M) for i in range(I))

problem += revenue - purchase_cost - storage_cost_total

# Solve the problem
problem.solve()

# Output
result = {
    "buy": [[pulp.value(buy[m][i]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[m][i]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[m][i]) for i in range(I)] for m in range(M + 1)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')