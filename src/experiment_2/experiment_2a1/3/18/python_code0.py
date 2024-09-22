import pulp
import json

# Data extraction from JSON format
data = {'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'SellPrice': 150, 'IsVegetable': [True, True, False, False, False], 'MaxVegetableRefiningPerMonth': 200, 'MaxNonVegetableRefiningPerMonth': 250, 'StorageSize': 1000, 'StorageCost': 5, 'MinHardness': 3, 'MaxHardness': 6, 'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'InitialAmount': 500}

M = data['M']
I = data['I']
buy_prices = data['BuyPrice']
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

# Initialize the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buy_quantity = pulp.LpVariable.dicts("buy_quantity", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, upBound=storage_size, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum((sell_price * pulp.lpSum(refine[i][m] for i in range(I)) - 
                     pulp.lpSum(buy_prices[m][i] * buy_quantity[i][m] for i in range(I)) - 
                     storage_cost * pulp.lpSum(storage[i][m] for i in range(I))) for m in range(M))

problem += profit

# Constraints
for m in range(M):
    for i in range(I):
        problem += refine[i][m] <= (max_veg if is_vegetable[i] else max_non_veg)
        
        if m > 0:
            problem += storage[i][m] == storage[i][m-1] + buy_quantity[i][m] - refine[i][m]

        if m == M - 1:
            problem += storage[i][m] == init_amount

# Storage constraint at the beginning
for i in range(I):
    problem += storage[i][0] == init_amount

# Hardness constraint
problem += (pulp.lpSum(hardness[i] * (refine[i][m] for i in range(I))) / pulp.lpSum(refine[i][m] for i in range(I)) >= min_hardness)
problem += (pulp.lpSum(hardness[i] * (refine[i][m] for i in range(I))) / pulp.lpSum(refine[i][m] for i in range(I)) <= max_hardness)

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "buy": [[pulp.value(buy_quantity[i][m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]
}

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')