import pulp

# Given data
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

M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_vegetable = data['MaxVegetableRefiningPerMonth']
max_non_vegetable = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

# Define problem
problem = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

# Variables
buy = pulp.LpVariable.dicts("Buy", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((m, i) for m in range(M+1) for i in range(I)), lowBound=0, upBound=storage_size, cat='Continuous')

# Objective function
profit = (
    pulp.lpSum(refine[m, i] * (sell_price - buy_price[m][i]) for m in range(M) for i in range(I)) -
    pulp.lpSum(storage_cost * storage[m, i] for m in range(M) for i in range(I))
)
problem += profit

# Constraints

# Initial storage constraint
for i in range(I):
    problem += storage[0, i] == init_amount

# Purchasing and refining balance, storage update
for m in range(M):
    for i in range(I):
        problem += storage[m+1, i] == storage[m, i] + buy[m, i] - refine[m, i]

# Refining constraints for vegetable and non-vegetable oils
for m in range(M):
    problem += pulp.lpSum(refine[m, i] for i in range(I) if is_vegetable[i]) <= max_vegetable
    problem += pulp.lpSum(refine[m, i] for i in range(I) if not is_vegetable[i]) <= max_non_vegetable

# Hardness constraints for the final product
for m in range(M):
    total_refined = pulp.lpSum(refine[m, i] for i in range(I))
    weighted_hardness = pulp.lpSum(hardness[i] * refine[m, i] for i in range(I))
    problem += weighted_hardness >= min_hardness * total_refined
    problem += weighted_hardness <= max_hardness * total_refined

# Final storage constraint
for i in range(I):
    problem += storage[M, i] == init_amount

# Solve the problem
problem.solve()

# Prepare output
solution = {
    "buy": [[pulp.value(buy[m, i]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[m, i]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[m, i]) for i in range(I)] for m in range(M+1)],
}

print(solution)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')