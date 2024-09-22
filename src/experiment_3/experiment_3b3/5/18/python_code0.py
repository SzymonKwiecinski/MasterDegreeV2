import pulp

# Extract the data
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

# Problem definition
problem = pulp.LpProblem("Oil_Refinery_Optimization", pulp.LpMaximize)

# Sets and Indices
M = data['M']
I = data['I']

# Parameters
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_veg = data['MaxVegetableRefiningPerMonth']
max_nveg = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

# Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(sell_price * pulp.lpSum(refine[i, m] for i in range(I)) 
                      - pulp.lpSum(buy_price[m][i] * buyquantity[i, m] for i in range(I))
                      - storage_cost * pulp.lpSum(storage[i, m] for i in range(I)) for m in range(M))

# Constraints
# Production Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_nveg

# Storage Constraints
for i in range(I):
    for m in range(M):
        if m > 0:
            problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == init_amount + buyquantity[i, m] - refine[i, m]
        problem += storage[i, m] <= storage_size

# Hardness Constraints
for m in range(M):
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) <= max_hardness * total_refine
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) >= min_hardness * total_refine

# Solve the problem
problem.solve()

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')