import json
import pulp

# Load data
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, upBound=storage_size, cat='Continuous')

# Objective function
profit = pulp.lpSum((sell_price * sum(refine[i][m] for i in range(I)) 
                     - pulp.lpSum(buyquantity[i][m] * buy_price[m][i] for i in range(I))) for m in range(M))
problem += profit

# Constraints
for m in range(M):
    # Refining constraints
    problem += (pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_vegetable_refining_per_month)
    problem += (pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_vegetable_refining_per_month)
    
    # Storage balance
    for i in range(I):
        if m == 0:
            problem += storage[i][m] == init_amount
        else:
            problem += storage[i][m] == storage[i][m - 1] + buyquantity[i][m] - refine[i][m]

# Last month storage constraint
for i in range(I):
    problem += storage[i][M - 1] == init_amount

# Hardness constraints
problem += (pulp.lpSum(hardness[i] * (refine[i][m] for i in range(I))) / 
                     (pulp.lpSum(refine[i][m] for i in range(I)) if pulp.lpSum(refine[i][m] for i in range(I)) > 0 else 1) 
                     >= min_hardness)
problem += (pulp.lpSum(hardness[i] * (refine[i][m] for i in range(I))) / 
                     (pulp.lpSum(refine[i][m] for i in range(I)) if pulp.lpSum(refine[i][m] for i in range(I)) > 0 else 1) 
                     <= max_hardness)

# Solve the problem
problem.solve()

# Prepare the output data
buy_output = [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)]
refine_output = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_output = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]

output = {
    "buy": buy_output,
    "refine": refine_output,
    "storage": storage_output
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')