import pulp
import json

# Data from JSON format
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

M = data['M']
I = data['I']
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

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M+1)), lowBound=0, upBound=StorageSize)

# Objective function
profit = pulp.lpSum(SellPrice * pulp.lpSum(refine[i][m] for i in range(I)) - 
                   pulp.lpSum(BuyPrice[m][i] * buyquantity[i][m] for i in range(I)) - 
                   StorageCost * pulp.lpSum(storage[i][m] for i in range(I)) for m in range(M))
problem += profit

# Storage balance constraints
for i in range(I):
    for m in range(1, M+1):
        problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"StorageBalance_{i}_{m}"

# Initial storage constraint
for i in range(I):
    problem += storage[i][0] == InitialAmount, f"InitialStorage_{i}"

# Final storage constraint
for i in range(I):
    problem += storage[i][M] == InitialAmount, f"FinalStorage_{i}"

# Vegetable refining constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if IsVegetable[i]) <= MaxVegetableRefiningPerMonth, f"MaxVegetableRefining_{m}"

# Non-vegetable refining constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not IsVegetable[i]) <= MaxNonVegetableRefiningPerMonth, f"MaxNonVegetableRefining_{m}"

# Hardness constraints
for m in range(M):
    problem += pulp.lpSum(Hardness[i] * refine[i][m] for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I)) >= MinHardness, f"MinHardness_{m}"
    problem += pulp.lpSum(Hardness[i] * refine[i][m] for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I)) <= MaxHardness, f"MaxHardness_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')