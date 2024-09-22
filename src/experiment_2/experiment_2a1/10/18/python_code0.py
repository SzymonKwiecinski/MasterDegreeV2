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

# Create the problem
problem = pulp.LpProblem("MaximizeProfit", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
problem += pulp.lpSum([(sell_price * pulp.lpSum(refine[i][m] for i in range(I))) - 
                         pulp.lpSum(buy_price[m][i] * buyquantity[i][m] for i in range(I)) - 
                         storage_cost * pulp.lpSum(storage[i][m] for i in range(I)) 
                        ) for m in range(M)])

# Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I)) <= max_vegetable_refining_per_month * sum(is_vegetable) + max_non_vegetable_refining_per_month * (I - sum(is_vegetable))
    
    for i in range(I):
        problem += storage[i][m] <= storage_size  # Storage limit

for i in range(I):
    problem += storage[i][0] == init_amount  # Initial amount condition
    problem += storage[i][M-1] == init_amount  # Final amount condition

for m in range(1, M):
    for i in range(I):
        problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]

# Hardness constraints
problem += pulp.lpSum(hardness[i] * (refine[i][m] for i in range(I))) / pulp.lpSum(refine[i][m] for i in range(I)) >= min_hardness
                      for m in range(M) if pulp.lpSum(refine[i][m] for i in range(I)) > 0)
problem += pulp.lpSum(hardness[i] * (refine[i][m] for i in range(I))) / pulp.lpSum(refine[i][m] for i in range(I)) <= max_hardness
                      for m in range(M) if pulp.lpSum(refine[i][m] for i in range(I)) > 0)

# Solve the problem
problem.solve()

# Prepare the output
buy_output = [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)]
refine_output = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_output = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]

output = {
    "buy": buy_output,
    "refine": refine_output,
    "storage": storage_output
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')