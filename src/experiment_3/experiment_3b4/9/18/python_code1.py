import pulp

# Problem Data
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

# Constants
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

# Initialize Problem
problem = pulp.LpProblem("Refinery_Scheduling", pulp.LpMaximize)

# Variables
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
buyquantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M + 1)), lowBound=0, upBound=StorageSize, cat='Continuous')

# Objective Function
objective = pulp.lpSum(
    SellPrice * pulp.lpSum(refine[i, m] for i in range(I)) -
    pulp.lpSum(BuyPrice[m][i] * buyquantity[i, m] + StorageCost * storage[i, m] for i in range(I))
    for m in range(M)
)
problem += objective

# Constraints
# Refining constraints
for m in range(M):
    # Vegetable refining constraints
    problem += pulp.lpSum(refine[i, m] for i in range(I) if IsVegetable[i]) <= MaxVegetableRefiningPerMonth
    # Non-vegetable refining constraints
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not IsVegetable[i]) <= MaxNonVegetableRefiningPerMonth

# Storage constraints
for i in range(I):
    # Initial storage balance
    problem += storage[i, 0] == InitialAmount

    # Monthly storage balance
    for m in range(1, M + 1):
        problem += (storage[i, m] == storage[i, m - 1] + buyquantity[i, m - 1] - refine[i, m - 1])

    # Ending storage balance
    problem += storage[i, M] == InitialAmount

# Hardness constraints
for m in range(M):
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    hardness_constraint = pulp.lpSum(Hardness[i] * refine[i, m] for i in range(I))
    
    # Avoiding division by zero by adding constraints only when total_refine > 0
    problem += (total_refine == 0) | (hardness_constraint >= MinHardness * total_refine)
    problem += (total_refine == 0) | (hardness_constraint <= MaxHardness * total_refine)

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')