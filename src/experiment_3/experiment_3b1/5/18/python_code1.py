import pulp
import json

# Input data
data = json.loads('{"M": 6, "I": 5, "BuyPrice": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "SellPrice": 150, "IsVegetable": [true, true, false, false, false], "MaxVegetableRefiningPerMonth": 200, "MaxNonVegetableRefiningPerMonth": 250, "StorageSize": 1000, "StorageCost": 5, "MinHardness": 3, "MaxHardness": 6, "Hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "InitialAmount": 500}')

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
initial_amount = data['InitialAmount']

# Create the problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Decision Variables
buy_quantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M + 1)), lowBound=0)  # Adjusted range here

# Objective Function
problem += pulp.lpSum(sell_price * pulp.lpSum(refine[i, m] for i in range(I)) - 
                      pulp.lpSum(buy_price[m][i] * buy_quantity[i, m] for i in range(I)) - 
                      storage_cost * pulp.lpSum(storage[i, m] for i in range(I)) for m in range(M))

# Storage Constraints
for i in range(I):
    for m in range(1, M + 1):  # Adjusted range here
        problem += storage[i, m] == storage[i, m-1] + buy_quantity[i, m] - refine[i, m]
    
    # Initial and final storage constraints
    problem += storage[i, 0] == initial_amount
    problem += storage[i, M] == initial_amount
    
    # Storage size constraints
    for m in range(M + 1):  # Adjusted range here
        problem += storage[i, m] <= storage_size

# Refining Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_veg

# Hardness Constraints
for m in range(M):
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) >= min_hardness * pulp.lpSum(refine[i, m] for i in range(I))
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) <= max_hardness * pulp.lpSum(refine[i, m] for i in range(I))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')