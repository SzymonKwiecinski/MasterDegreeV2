import pulp

# Provided data
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
max_veg_refining = data['MaxVegetableRefiningPerMonth']
max_non_veg_refining = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

# Create the Linear Program
problem = pulp.LpProblem("Oil_Manufacturing", pulp.LpMaximize)

# Decision Variables
buy = pulp.LpVariable.dicts("Buy", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, upBound=storage_size, cat='Continuous')

# Objective Function: Maximize Profit
total_revenue = pulp.lpSum(refine[(i, m)] * sell_price for i in range(I) for m in range(M))
total_cost = pulp.lpSum(buy[(i, m)] * buy_price[m][i] for i in range(I) for m in range(M))
total_storage_cost = pulp.lpSum(storage[(i, m)] * storage_cost for i in range(I) for m in range(M))
problem += total_revenue - total_cost - total_storage_cost

# Constraints

# Initial Storage
for i in range(I):
    problem += storage[(i, 0)] == init_amount

# Balance Constraints for each month and oil
for m in range(M):
    for i in range(I):
        if m == 0:
            problem += buy[(i, m)] + init_amount == refine[(i, m)] + storage[(i, m+1)]
        else:
            problem += buy[(i, m)] + storage[(i, m)] == refine[(i, m)] + storage[(i, m+1)]

# Refining Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(refine[(i, m)] for i in range(I) if is_vegetable[i]) <= max_veg_refining
    problem += pulp.lpSum(refine[(i, m)] for i in range(I) if not is_vegetable[i]) <= max_non_veg_refining

# Hardness Constraints
for m in range(M):
    problem += pulp.lpSum((hardness[i] * refine[(i, m)]) for i in range(I)) <= max_hardness * pulp.lpSum(refine[(i, m)] for i in range(I))
    problem += pulp.lpSum((hardness[i] * refine[(i, m)]) for i in range(I)) >= min_hardness * pulp.lpSum(refine[(i, m)] for i in range(I))

# End of period storage must be equal to initial amount
for i in range(I):
    problem += storage[(i, M)] == init_amount

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "buy": [[pulp.value(buy[(i, m)]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[(i, m)]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[(i, m)]) for i in range(I)] for m in range(M+1)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')