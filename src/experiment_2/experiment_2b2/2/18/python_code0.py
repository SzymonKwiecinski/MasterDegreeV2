import pulp

# Extract data from the JSON format provided
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

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Extract key data
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

# Decision variables
buy = pulp.LpVariable.dicts("Buy", ((m, i) for m in range(M) for i in range(I)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", ((m, i) for m in range(M) for i in range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((m, i) for m in range(M) for i in range(I)), lowBound=0, upBound=storage_size)

# Objective function: Maximize profit
profit = pulp.lpSum([
    (sell_price - buy_price[m][i]) * refine[(m, i)] - storage_cost * storage[(m, i)]
    for m in range(M) for i in range(I)
])
problem += profit

# Constraints

# Initial storage constraint before month 0
for i in range(I):
    problem += storage[(0, i)] == init_amount

# Storage and refining balance
for m in range(1, M + 1):
    for i in range(I):
        problem += storage[(m, i)] == storage[(m - 1, i)] + buy[(m - 1, i)] - refine[(m - 1, i)]

# Refining capacity constraints
for m in range(M):
    problem += pulp.lpSum(refine[(m, i)] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[(m, i)] for i in range(I) if not is_vegetable[i]) <= max_non_veg

# Hardness constraint
for m in range(M):
    total_refined = pulp.lpSum(refine[(m, i)] for i in range(I))
    if total_refined > 0:
        hardness_weighted_sum = pulp.lpSum(refine[(m, i)] * hardness[i] for i in range(I))
        problem += (hardness_weighted_sum / total_refined >= min_hardness)
        problem += (hardness_weighted_sum / total_refined <= max_hardness)

# Final storage should be equal to the initial amount
for i in range(I):
    problem += storage[(M - 1, i)] == init_amount

# Solve the problem
problem.solve()

# Extract results
buy_solution = [[pulp.value(buy[(m, i)]) for i in range(I)] for m in range(M)]
refine_solution = [[pulp.value(refine[(m, i)]) for i in range(I)] for m in range(M)]
storage_solution = [[pulp.value(storage[(m, i)]) for i in range(I)] for m in range(M)]

# Output the results
output = {
    "buy": buy_solution,
    "refine": refine_solution,
    "storage": storage_solution
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')