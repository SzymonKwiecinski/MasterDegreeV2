import pulp

# Data
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

# Constants
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

# Problem
problem = pulp.LpProblem("Oil_Refining_and_Blending", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat='Continuous')

# Objective Function
profit = (sell_price * pulp.lpSum(refine[i, m] for i in range(I) for m in range(M)) -
          pulp.lpSum(buy_price[m][i] * buyquantity[i, m] for i in range(I) for m in range(M)) -
          storage_cost * pulp.lpSum(storage[i, m] for i in range(I) for m in range(M)))

problem += profit

# Constraints
for m in range(M):
    # Refining Constraints
    problem += pulp.lpSum(is_vegetable[i] * refine[i, m] for i in range(I)) <= max_veg
    problem += pulp.lpSum((1 - is_vegetable[i]) * refine[i, m] for i in range(I)) <= max_non_veg
    
    # Hardness Constraint
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    if total_refine:
        problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / total_refine <= max_hardness
        problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / total_refine >= min_hardness

    for i in range(I):
        # Storage Constraints
        if m == 0:
            problem += storage[i, m] == init_amount + buyquantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]
        
        problem += storage[i, m] <= storage_size

# End of Period Storage Constraint
for i in range(I):
    problem += storage[i, M] == init_amount

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')