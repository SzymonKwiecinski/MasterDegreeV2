import pulp

# Data
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

# Variables
M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_vegetable = data['MaxVegetableRefiningPerMonth']
max_non_vegetable = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
max_hardness = data['MaxHardness']
min_hardness = data['MinHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buy = pulp.LpVariable.dicts("buy", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M + 1)), lowBound=0, cat='Continuous')

# Initial Storage
for i in range(I):
    problem += storage[i, 0] == init_amount

# Constraints
# Storage balance
for m in range(M):
    for i in range(I):
        problem += (
            storage[i, m] + buy[i, m] == refine[i, m] + storage[i, m + 1]
        )
        
# Refining capacity
for m in range(M):
    problem += (
        pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_vegetable
    )
    problem += (
        pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_vegetable
    )

# Storage capacity
for m in range(M):
    for i in range(I):
        problem += storage[i, m + 1] <= storage_size

# Hardness constraint
for m in range(M):
    problem += (
        pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) <= max_hardness * pulp.lpSum(refine[i, m] for i in range(I))
    )
    problem += (
        pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) >= min_hardness * pulp.lpSum(refine[i, m] for i in range(I))
    )

# End-month storage requirement
for i in range(I):
    problem += storage[i, M] == init_amount

# Objective
revenue = pulp.lpSum(sell_price * pulp.lpSum(refine[i, m] for i in range(I)) for m in range(M))
costs = pulp.lpSum(buy_price[m][i] * buy[i, m] + storage_cost * storage[i, m] for i in range(I) for m in range(M))
problem += revenue - costs

# Solve
problem.solve()

# Output Results
buy_result = [[buy[i, m].varValue for i in range(I)] for m in range(M)]
refine_result = [[refine[i, m].varValue for i in range(I)] for m in range(M)]
storage_result = [[storage[i, m].varValue for i in range(I)] for m in range(M + 1)]

result = {
    "buy": buy_result,
    "refine": refine_result,
    "storage": storage_result
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')