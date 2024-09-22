import pulp
import json

data = {'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], 
        [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], 
        [90, 100, 140, 80, 135]], 'SellPrice': 150, 
        'IsVegetable': [True, True, False, False, False], 
        'MaxVegetableRefiningPerMonth': 200, 
        'MaxNonVegetableRefiningPerMonth': 250, 
        'StorageSize': 1000, 
        'StorageCost': 5, 
        'MinHardness': 3, 
        'MaxHardness': 6, 
        'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 
        'InitialAmount': 500}

# Constants from input data
M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_veg = data['MaxVegetableRefiningPerMonth']
max_veg = data['MaxVegetableRefiningPerMonth']
max_non_veg = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in range(I) for m in range(M)) - 
                    pulp.lpSum(buy_price[m][i] * buyquantity[i][m] for i in range(I) for m in range(M)) - 
                    pulp.lpSum(storage_cost * storage[i][m] for i in range(I) for m in range(M)))

problem += profit

# Constraints
# Monthly refining capacity constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_veg

# Storage constraints for each oil
for m in range(M):
    for i in range(I):
        problem += storage[i][m] <= storage_size

# Hardness constraints
for m in range(M):
    problem += (pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / 
                 pulp.lpSum(refine[i][m] for i in range(I)) <= max_hardness)
    problem += (pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / 
                 pulp.lpSum(refine[i][m] for i in range(I)) >= min_hardness)

# Initial and final storage constraints
for i in range(I):
    problem += storage[i][0] == init_amount
    problem += storage[i][M-1] == init_amount

# Storage balance for each month
for m in range(1, M):
    for i in range(I):
        problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m-1] - refine[i][m-1]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "buy": [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]
}

print(json.dumps(output))

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')