import pulp
import json

# Data from the input
data = {'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'SellPrice': 150, 'IsVegetable': [True, True, False, False, False], 'MaxVegetableRefiningPerMonth': 200, 'MaxNonVegetableRefiningPerMonth': 250, 'StorageSize': 1000, 'StorageCost': 5, 'MinHardness': 3, 'MaxHardness': 6, 'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'InitialAmount': 500}

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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in range(I) for m in range(M)) -
                      pulp.lpSum(buy_price[m][i] * buyquantity[i][m] for i in range(I) for m in range(M)) -
                      pulp.lpSum(storage_cost * storage[i][m] for i in range(I) for m in range(M))), "Total_Profit"

# Constraints
for m in range(M):
    # Refining capacity constraints
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_veg, f"Max_Vegetable_Refining_{m}")
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_veg, f"Max_NonVegetable_Refining_{m}")

    for i in range(I):
        # Storage constraints
        if m == 0:
            problem += storage[i][m] == init_amount, f"Init_Storage_{i}"
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"Storage_Balance_{i}_{m}"

        # Storage capacity constraint
        problem += storage[i][m] <= storage_size, f"Max_Storage_{i}_{m}"

# Last month storage constraint
for i in range(I):
    problem += storage[i][M-1] == init_amount, f"Final_Storage_{i}"

# Hardness constraint
problem += pulp.lpSum(hardness[i] * (pulp.lpSum(refine[i][m] for m in range(M)) / pulp.lpSum(refine[i][m] for i in range(I) for m in range(M)))) for i in range(I) if pulp.lpSum(refine[i][m] for m in range(M)) > 0) >= min_hardness, "Min_Hardness"
problem += pulp.lpSum(hardness[i] * (pulp.lpSum(refine[i][m] for m in range(M)) / pulp.lpSum(refine[i][m] for i in range(I) for m in range(M)))) for i in range(I) if pulp.lpSum(refine[i][m] for m in range(M)) > 0) <= max_hardness, "Max_Hardness"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "buy": [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')