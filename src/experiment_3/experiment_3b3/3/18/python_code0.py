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

# Parameters
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
buyquantity = pulp.LpVariable.dicts("BuyQuantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", (range(I), range(M+1)), lowBound=0)

# Objective Function
profit = (
    pulp.lpSum(sell_price * refine[i][m] for i in range(I) for m in range(M))
    - pulp.lpSum(buy_price[m][i] * buyquantity[i][m] for i in range(I) for m in range(M))
    - pulp.lpSum(storage_cost * storage[i][m] for i in range(I) for m in range(M))
)
problem += profit

# Constraints
for i in range(I):
    problem += storage[i][0] == init_amount

for m in range(M):
    for i in range(I):
        problem += storage[i][m+1] == storage[i][m] + buyquantity[i][m] - refine[i][m]
        problem += storage[i][m] <= storage_size

    veg_indices = [i for i in range(I) if is_vegetable[i]]
    non_veg_indices = [i for i in range(I) if not is_vegetable[i]]

    problem += pulp.lpSum(refine[i][m] for i in veg_indices) <= max_veg
    problem += pulp.lpSum(refine[i][m] for i in non_veg_indices) <= max_non_veg

    hardness_contribution = pulp.lpSum(hardness[i] * refine[i][m] for i in range(I))
    total_refined = pulp.lpSum(refine[i][m] for i in range(I))

    if total_refined > 0:
        problem += min_hardness * total_refined <= hardness_contribution
        problem += hardness_contribution <= max_hardness * total_refined

for i in range(I):
    problem += storage[i][M] == init_amount

# Solve
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')