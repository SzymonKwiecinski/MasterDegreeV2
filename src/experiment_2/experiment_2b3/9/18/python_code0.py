import pulp

# Data provided in JSON format
data = {
    "M": 6, 
    "I": 5, 
    "BuyPrice": [
        [110, 120, 130, 110, 115], 
        [130, 130, 110, 90, 115], 
        [110, 140, 130, 100, 95], 
        [120, 110, 120, 120, 125], 
        [100, 120, 150, 110, 105], 
        [90, 100, 140, 80, 135]
    ], 
    "SellPrice": 150, 
    "IsVegetable": [True, True, False, False, False], 
    "MaxVegetableRefiningPerMonth": 200, 
    "MaxNonVegetableRefiningPerMonth": 250, 
    "StorageSize": 1000, 
    "StorageCost": 5, 
    "MinHardness": 3, 
    "MaxHardness": 6, 
    "Hardness": [8.8, 6.1, 2.0, 4.2, 5.0], 
    "InitialAmount": 500
}

M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_veg = data['MaxVegetableRefiningPerMonth']
max_non_veg = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
max_hardness = data['MaxHardness']
min_hardness = data['MinHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

# Define the problem
problem = pulp.LpProblem("OilBlendingMaxProfit", pulp.LpMaximize)

# Variables
buy = pulp.LpVariable.dicts("Buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(I), range(M + 1)), lowBound=0, cat='Continuous')

# Initial storage condition (Month 0)
for i in range(I):
    problem += storage[i][0] == init_amount

# Objective function: Maximize profit
total_revenue = pulp.lpSum(refine[i][m] * sell_price for i in range(I) for m in range(M))
total_cost = pulp.lpSum(buy[i][m] * buy_price[m][i] + storage_cost * storage[i][m + 1] for i in range(I) for m in range(M))
problem += total_revenue - total_cost

# Constraints
for m in range(M):
    # Refining capacity constraints
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_veg

    # Hardness constraints
    problem += pulp.lpSum(refine[i][m] * hardness[i] for i in range(I)) >= min_hardness * pulp.lpSum(refine[i][m] for i in range(I))
    problem += pulp.lpSum(refine[i][m] * hardness[i] for i in range(I)) <= max_hardness * pulp.lpSum(refine[i][m] for i in range(I))

    for i in range(I):
        # Storage dynamics constraints
        problem += storage[i][m + 1] == storage[i][m] + buy[i][m] - refine[i][m]

        # Storage capacity constraints
        problem += storage[i][m + 1] <= storage_size

# End of period storage requirement
for i in range(I):
    problem += storage[i][M] == init_amount

# Solve the problem
problem.solve()

# Generate the output format
output = {
    "buy": [[pulp.value(buy[i][m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M + 1)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')