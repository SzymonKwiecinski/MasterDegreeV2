import pulp
import json

# Data parsing
data_json = '''{'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'SellPrice': 150, 'IsVegetable': [True, True, False, False, False], 'MaxVegetableRefiningPerMonth': 200, 'MaxNonVegetableRefiningPerMonth': 250, 'StorageSize': 1000, 'StorageCost': 5, 'MinHardness': 3, 'MaxHardness': 6, 'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'InitialAmount': 500}'''
data = json.loads(data_json)

# Parameters
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
initial_amount = data['InitialAmount']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
buy_quantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, upBound=storage_size)

# Objective Function
profit_terms = pulp.lpSum([
    (sell_price * refine[i][m] for i in range(I)) - 
    (pulp.lpSum(buy_price[m][i] * buy_quantity[i][m] for i in range(I))) - 
    (storage_cost * pulp.lpSum(storage[i][m] for i in range(I)))
    for m in range(M)
])
problem += profit_terms

# Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_vegetable_refining_per_month
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_vegetable_refining_per_month
    
    for i in range(I):
        if m > 0:
            problem += storage[i][m] == storage[i][m - 1] + buy_quantity[i][m] - refine[i][m]
        else:
            problem += storage[i][m] == initial_amount

    problem += (pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / 
                 pulp.lpSum(refine[i][m] for i in range(I))) >= min_hardness
    problem += (pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / 
                 pulp.lpSum(refine[i][m] for i in range(I))) <= max_hardness

for i in range(I):
    problem += storage[i][M] == initial_amount

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')