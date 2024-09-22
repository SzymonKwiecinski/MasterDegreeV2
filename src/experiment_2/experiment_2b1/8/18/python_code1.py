import pulp
import json

# Input data
data = {'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'SellPrice': 150, 'IsVegetable': [True, True, False, False, False], 'MaxVegetableRefiningPerMonth': 200, 'MaxNonVegetableRefiningPerMonth': 250, 'StorageSize': 1000, 'StorageCost': 5, 'MinHardness': 3, 'MaxHardness': 6, 'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'InitialAmount': 500}

# Setup
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

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, upBound=storage_size, cat='Continuous')

# Objective Function
profit = pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in range(I) for m in range(M))) \
           - pulp.lpSum(buy_price[m][i] * buyquantity[i][m] for i in range(I) for m in range(M)) \
           - storage_cost * pulp.lpSum(storage[i][m] for i in range(I) for m in range(M))
problem += profit

# Constraints
for m in range(M):
    # Refining limits
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_veg, f"MaxVegRefineMonth{m}")
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_veg, f"MaxNonVegRefineMonth{m}")

    # Storage updates
    for i in range(I):
        if m == 0:
            problem += storage[i][m] == init_amount, f"InitialStorage{i}"
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"StorageUpdate{i}_{m}"

    # Hardness constraint
    total_refine = pulp.lpSum(refine[i][m] for i in range(I))
    hardness_constraint = pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / total_refine if total_refine > 0 else 0
    problem += hardness_constraint >= min_hardness, f"MinHardness{m}"
    problem += hardness_constraint <= max_hardness, f"MaxHardness{m}"

# Last month storage condition
for i in range(I):
    problem += storage[i][M-1] == init_amount, f"FinalStorage{i}"

# Solve the problem
problem.solve()

# Output results
buy = [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)]
refine_output = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_output = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]

output = {
    "buy": buy,
    "refine": refine_output,
    "storage": storage_output
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')