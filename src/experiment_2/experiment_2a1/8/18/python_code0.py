import pulp
import json

data = {'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'SellPrice': 150, 'IsVegetable': [True, True, False, False, False], 'MaxVegetableRefiningPerMonth': 200, 'MaxNonVegetableRefiningPerMonth': 250, 'StorageSize': 1000, 'StorageCost': 5, 'MinHardness': 3, 'MaxHardness': 6, 'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'InitialAmount': 500}

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

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, upBound=storage_size)

# Objective function: Maximize profit
profit = pulp.lpSum((sell_price * pulp.lpSum(refine[i][m] for i in range(I)) - 
                     pulp.lpSum(buyquantity[i][m] * buy_price[m][i] for i in range(I)) - 
                     pulp.lpSum(storage_cost * storage[i][m] for i in range(I))) for m in range(M))
problem += profit

# Constraints
for m in range(M):
    for i in range(I):
        if is_vegetable[i]:
            problem += pulp.lpSum(refine[i][m] for m in range(M)) <= max_veg, f"Max_Veg_Refine_Month_{m}"
        else:
            problem += pulp.lpSum(refine[i][m] for m in range(M)) <= max_non_veg, f"Max_Non_Veg_Refine_Month_{m}"

for m in range(M):
    for i in range(I):
        problem += storage[i][m] == (storage[i][m-1] + buyquantity[i][m] - refine[i][m]) if m > 0 else init_amount, f"Storage_Constraint_{i}_{m}"

# Final month storage constraint
for i in range(I):
    problem += storage[i][M-1] == init_amount, f"Final_Storage_Constraint_{i}"

# Hardness constraint
for m in range(M):
    problem += (pulp.lpSum(refine[i][m] * hardness[i] for i in range(I)) / 
                 pulp.lpSum(refine[i][m] for i in range(I))) >= min_hardness, f"Min_Hardness_Constraint_{m}"
    )
    problem += (pulp.lpSum(refine[i][m] * hardness[i] for i in range(I)) / 
                 pulp.lpSum(refine[i][m] for i in range(I))) <= max_hardness, f"Max_Hardness_Constraint_{m}"
    )

# Solve the problem
problem.solve()

# Extract results
buy_results = [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)]
refine_results = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_results = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]

# Output results
output = {
    "buy": buy_results,
    "refine": refine_results,
    "storage": storage_results
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')