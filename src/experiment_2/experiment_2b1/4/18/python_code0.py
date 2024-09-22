import pulp
import json

# Input data
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

# Constants from input
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
buy_quantity = pulp.LpVariable.dicts("buy_quantity", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in range(I) for m in range(M)) 
                    - pulp.lpSum(buy_price[m][i] * buy_quantity[i][m] for i in range(I) for m in range(M)) 
                    - storage_cost * pulp.lpSum(storage[i][m] for i in range(I) for m in range(M)))
problem += profit

# Constraints for storage and refining
for m in range(M):
    for i in range(I):
        if is_vegetable[i]:
            problem += pulp.lpSum(refine[i][m] for m in range(M)) <= max_veg
        else:
            problem += pulp.lpSum(refine[i][m] for m in range(M)) <= max_non_veg
            
        # Storage update constraints
        if m == 0:
            problem += storage[i][0] == init_amount
        else:
            problem += storage[i][m] == storage[i][m-1] + buy_quantity[i][m] - refine[i][m]

    # Hardness constraints
    hardness_avg = pulp.lpSum(hardness[i] * (refine[i][m] / pulp.lpSum(refine[j][m] for j in range(I))) 
                               for i in range(I) if pulp.lpSum(refine[j][m] for j in range(I)) > 0)
    problem += hardness_avg >= min_hardness
    problem += hardness_avg <= max_hardness

# Last month storage constraint
for i in range(I):
    problem += storage[i][M - 1] == init_amount

# Solve the problem
problem.solve()

# Prepare output
result = {
    "buy": [[buy_quantity[i][m].varValue for i in range(I)] for m in range(M)],
    "refine": [[refine[i][m].varValue for i in range(I)] for m in range(M)],
    "storage": [[storage[i][m].varValue for i in range(I)] for m in range(M)]
}

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# If you want to see the result in a specific format, simply uncomment the next line
# print(json.dumps(result))