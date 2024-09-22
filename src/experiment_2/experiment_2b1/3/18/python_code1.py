import pulp
import json

# Input data
data = {'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'SellPrice': 150, 'IsVegetable': [True, True, False, False, False], 'MaxVegetableRefiningPerMonth': 200, 'MaxNonVegetableRefiningPerMonth': 250, 'StorageSize': 1000, 'StorageCost': 5, 'MinHardness': 3, 'MaxHardness': 6, 'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'InitialAmount': 500}

M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_vegetable_refining_per_month = data['MaxVegetableRefiningPerMonth']
max_non_vegetable_refining_per_month = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
buyquantity = pulp.LpVariable.dicts("buy", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(sell_price * sum(refine[i, m] for i in range(I) for m in range(M)) - 
                    pulp.lpSum(buy_price[m][i] * buyquantity[i, m] for i in range(I) for m in range(M)) - 
                    storage_cost * pulp.lpSum(storage[i, m] for i in range(I) for m in range(M)))

problem += profit, "Total_Profit"

# Constraints
for m in range(M):
    total_vegetable_refining = pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i])
    total_non_vegetable_refining = pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i])
    
    problem += total_vegetable_refining <= max_vegetable_refining_per_month, f"MaxVegetableRefining_{m}"
    problem += total_non_vegetable_refining <= max_non_vegetable_refining_per_month, f"MaxNonVegetableRefining_{m}"
    
    for i in range(I):
        problem += storage[i, m] <= storage_size, f"MaxStorage_{i}_{m}"

        # Storage balance constraint
        if m > 0:
            problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m], f"StorageBalance_{i}_{m}"
        else:
            problem += storage[i, m] == init_amount + buyquantity[i, m] - refine[i, m], f"InitialStorageBalance_{i}"

# Hardness constraints
for m in range(M):
    total_refined = pulp.lpSum(refine[i, m] for i in range(I))
    if total_refined > 0:  # To avoid division by zero
        problem += (pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / total_refined >= min_hardness), f"MinHardness_{m}"
        problem += (pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / total_refined <= max_hardness), f"MaxHardness_{m}"

# Final storage constraint
for i in range(I):
    problem += storage[i, M-1] == init_amount, f"FinalStorageBalance_{i}"

# Solve the problem
problem.solve()

# Output results
buy_result = [[pulp.value(buyquantity[i, m]) for i in range(I)] for m in range(M)]
refine_result = [[pulp.value(refine[i, m]) for i in range(I)] for m in range(M)]
storage_result = [[pulp.value(storage[i, m]) for i in range(I)] for m in range(M)]

output = {
    "buy": buy_result,
    "refine": refine_result,
    "storage": storage_result
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')