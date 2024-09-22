import pulp
import json

data = {'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'SellPrice': 150, 'IsVegetable': [True, True, False, False, False], 'MaxVegetableRefiningPerMonth': 200, 'MaxNonVegetableRefiningPerMonth': 250, 'StorageSize': 1000, 'StorageCost': 5, 'MinHardness': 3, 'MaxHardness': 6, 'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'InitialAmount': 500}

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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQty", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in range(I) for m in range(M)) - 
                    pulp.lpSum(buy_price[m][i] * buyquantity[i][m] for i in range(I) for m in range(M)) - 
                    storage_cost * pulp.lpSum(storage[i][m] for i in range(I) for m in range(M)))

problem += profit

# Constraints
for m in range(M):
    # Refining constraints
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_veg, f"MaxVegRefineMonth_{m}"
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_veg, f"MaxNonVegRefineMonth_{m}"

    for i in range(I):
        # Storage constraints: can't exceed storage size
        problem += storage[i][m] <= storage_size, f"StorageSize_{i}_{m}"

        # Update storage: for each oil
        if m > 0:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"StorageUpdate_{i}_{m}"
        else:
            problem += storage[i][m] == init_amount + buyquantity[i][m] - refine[i][m], f"InitialStorageUpdate_{i}_{m}"

# Hardness constraints
problem += pulp.lpSum(hardness[i] * pulp.lpSum(refine[i][m] for m in range(M)) for i in range(I)) / \
                      pulp.lpSum(refine[i][m] for i in range(I) for m in range(M)) >= min_hardness, "MinHardness"
problem += pulp.lpSum(hardness[i] * pulp.lpSum(refine[i][m] for m in range(M)) for i in range(I)) / \
                      pulp.lpSum(refine[i][m] for i in range(I) for m in range(M)) <= max_hardness, "MaxHardness"

# Storage constraint for the last month must equal initial amount
for i in range(I):
    problem += storage[i][M-1] == init_amount, f"FinalStorageEqualInit_{i}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "buy": [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')