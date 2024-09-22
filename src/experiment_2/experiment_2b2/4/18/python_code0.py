import pulp

# Data
data = {
    'M': 6,
    'I': 5,
    'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], 
                 [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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

# Unpack Data
M = data['M']
I = data['I']
BuyPrice = data['BuyPrice']
SellPrice = data['SellPrice']
IsVegetable = data['IsVegetable']
MaxVegetableRefining = data['MaxVegetableRefiningPerMonth']
MaxNonVegetableRefining = data['MaxNonVegetableRefiningPerMonth']
StorageSize = data['StorageSize']
StorageCost = data['StorageCost']
MinHardness = data['MinHardness']
MaxHardness = data['MaxHardness']
Hardness = data['Hardness']
InitialAmount = data['InitialAmount']

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
buy = pulp.LpVariable.dicts("Buy", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((m, i) for m in range(M+1) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
total_revenue = pulp.lpSum(SellPrice * pulp.lpSum(refine[m, i] for i in range(I)) for m in range(M))
total_buy_costs = pulp.lpSum(BuyPrice[m][i] * buy[m, i] for m in range(M) for i in range(I))
total_storage_costs = pulp.lpSum(StorageCost * storage[m, i] for m in range(1, M+1) for i in range(I))

problem += total_revenue - total_buy_costs - total_storage_costs

# Constraints
# Initial storage
for i in range(I):
    problem += storage[0, i] == InitialAmount

# Balance equations
for m in range(M):
    for i in range(I):
        problem += storage[m, i] + buy[m, i] == refine[m, i] + storage[m+1, i]

# Storage limits
for m in range(1, M+1):
    for i in range(I):
        problem += storage[m, i] <= StorageSize

# Refining limits
for m in range(M):
    problem += pulp.lpSum(refine[m, i] for i in range(I) if IsVegetable[i]) <= MaxVegetableRefining
    problem += pulp.lpSum(refine[m, i] for i in range(I) if not IsVegetable[i]) <= MaxNonVegetableRefining

# Hardness constraints
for m in range(M):
    total_refine = pulp.lpSum(refine[m, i] for i in range(I))
    weighted_hardness = pulp.lpSum(refine[m, i] * Hardness[i] for i in range(I))
    if total_refine > 0:
        problem += weighted_hardness <= MaxHardness * total_refine
        problem += weighted_hardness >= MinHardness * total_refine

# Final storage equal to initial storage
for i in range(I):
    problem += storage[M, i] == InitialAmount

# Solve
problem.solve()

# Results
buy_quantity = [[pulp.value(buy[m, i]) for i in range(I)] for m in range(M)]
refine_quantity = [[pulp.value(refine[m, i]) for i in range(I)] for m in range(M)]
storage_quantity = [[pulp.value(storage[m, i]) for i in range(I)] for m in range(M+1)]

result = {
    "buy": buy_quantity,
    "refine": refine_quantity,
    "storage": storage_quantity
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')