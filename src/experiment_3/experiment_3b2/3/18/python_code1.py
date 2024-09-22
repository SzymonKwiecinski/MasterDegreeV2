import pulp
import json

# Given data in JSON format
data = json.loads('{"M": 6, "I": 5, "BuyPrice": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "SellPrice": 150, "IsVegetable": [true, true, false, false, false], "MaxVegetableRefiningPerMonth": 200, "MaxNonVegetableRefiningPerMonth": 250, "StorageSize": 1000, "StorageCost": 5, "MinHardness": 3, "MaxHardness": 6, "Hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "InitialAmount": 500}')

M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_vegetable_refining = data['MaxVegetableRefiningPerMonth']
max_non_vegetable_refining = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
initial_amount = data['InitialAmount']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
refine = pulp.LpVariable.dicts("Refine", (range(I), range(M)), lowBound=0, cat='Continuous')
buyquantity = pulp.LpVariable.dicts("BuyQuantity", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(I), range(M)), lowBound=0, upBound=storage_size, cat='Continuous')

# Objective Function
objective = pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in range(I)) for m in range(M)) - \
                       pulp.lpSum(buy_price[m][i] * buyquantity[i][m] for m in range(M) for i in range(I)) - \
                       storage_cost * pulp.lpSum(storage[i][m] for m in range(I) for m in range(M))

problem += objective

# Storage Balance Constraints
for m in range(M):
    for i in range(I):
        if m == 0:
            problem += storage[i][m] == initial_amount + buyquantity[i][m] - refine[i][m]
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]

# Refining Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_vegetable_refining
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_vegetable_refining

# Storage Capacity Constraints
for m in range(M):
    for i in range(I):
        problem += storage[i][m] <= storage_size

# Hardness Constraints
for m in range(M):
    if pulp.lpSum(refine[i][m] for i in range(I)) > 0:
        problem += (pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / 
                    pulp.lpSum(refine[i][m] for i in range(I)) >= min_hardness)
        problem += (pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / 
                    pulp.lpSum(refine[i][m] for i in range(I)) <= max_hardness)

# Final Storage Constraints
for i in range(I):
    problem += storage[i][M-1] == initial_amount

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')