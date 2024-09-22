import pulp

# Data
data = {
    'M': 6, 
    'I': 5, 
    'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 
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

M, I = data['M'], data['I']
BuyPrice = data['BuyPrice']
SellPrice = data['SellPrice']
IsVegetable = data['IsVegetable']
MaxVegetableRefiningPerMonth = data['MaxVegetableRefiningPerMonth']
MaxNonVegetableRefiningPerMonth = data['MaxNonVegetableRefiningPerMonth']
StorageSize = data['StorageSize']
StorageCost = data['StorageCost']
MinHardness = data['MinHardness']
MaxHardness = data['MaxHardness']
Hardness = data['Hardness']
InitialAmount = data['InitialAmount']

# Problem
problem = pulp.LpProblem("Refinery_Optimization", pulp.LpMaximize)

# Variables
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M+1)), lowBound=0, cat='Continuous')

# Objective
first_sum = pulp.lpSum(SellPrice * pulp.lpSum(refine[i][m] for i in range(I)) for m in range(M))
second_sum = pulp.lpSum(BuyPrice[m][i] * buyquantity[i][m] + StorageCost * storage[i][m] for i in range(I) for m in range(M))
problem += first_sum - second_sum

# Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if IsVegetable[i]) <= MaxVegetableRefiningPerMonth
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not IsVegetable[i]) <= MaxNonVegetableRefiningPerMonth

for i in range(I):
    for m in range(M):
        problem += storage[i][m] <= StorageSize
        if m == 0:
            problem += storage[i][m] == InitialAmount
        problem += storage[i][m] + buyquantity[i][m] == refine[i][m] + storage[i][m+1]

for i in range(I):
    problem += storage[i][M] == InitialAmount

for m in range(M):
    refine_sum = pulp.lpSum(refine[i][m] for i in range(I))
    hardness_weighted_sum = pulp.lpSum(Hardness[i] * refine[i][m] for i in range(I))
    problem += (refine_sum == 0) | (hardness_weighted_sum / refine_sum >= MinHardness)
    problem += (refine_sum == 0) | (hardness_weighted_sum / refine_sum <= MaxHardness)

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')