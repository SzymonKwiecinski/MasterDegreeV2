import pulp

# Read data from JSON
data = {
    'M': 6, 
    'I': 5, 
    'BuyPrice': [
        [110, 120, 130, 110, 115], 
        [130, 130, 110, 90, 115], 
        [110, 140, 130, 100, 95], 
        [120, 110, 120, 120, 125], 
        [100, 120, 150, 110, 105], 
        [90, 100, 140, 80, 135]
    ], 
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

# Constants
M = data['M']
I = data['I']
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

# Index 
months = range(M)
oils = range(I)

# Decision variables
buy_quantity = pulp.LpVariable.dicts("Buy", (months, oils), lowBound=0, cat='Continuous')
refine_quantity = pulp.LpVariable.dicts("Refine", (months, oils), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (months, oils), lowBound=0, cat='Continuous')

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective function
total_revenue = pulp.lpSum(refine_quantity[m][i] * sell_price for m in months for i in oils)
total_buying_cost = pulp.lpSum(buy_quantity[m][i] * data['BuyPrice'][m][i] for m in months for i in oils)
total_storage_cost = pulp.lpSum(storage[m][i] * storage_cost for m in months for i in oils)

problem += total_revenue - total_buying_cost - total_storage_cost

# Constraints

# Initial storage
for i in oils:
    problem += storage[0][i] == init_amount

# Storage balance and refining constraints
for m in months:
    for i in oils:
        if m == 0:
            continue
        problem += storage[m][i] == storage[m-1][i] + buy_quantity[m][i] - refine_quantity[m][i]

# Refining capacity constraints
for m in months:
    problem += pulp.lpSum(refine_quantity[m][i] for i in oils if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine_quantity[m][i] for i in oils if not is_vegetable[i]) <= max_non_veg

# Hardness constraints
for m in months:
    refine_total = pulp.lpSum(refine_quantity[m][i] for i in oils)
    if refine_total > 0:
        problem += pulp.lpSum(refine_quantity[m][i] * hardness[i] for i in oils) / refine_total <= max_hardness
        problem += pulp.lpSum(refine_quantity[m][i] * hardness[i] for i in oils) / refine_total >= min_hardness

# Storage capacity constraints
for m in months:
    for i in oils:
        problem += storage[m][i] <= storage_size

# Final storage constraint
for i in oils:
    problem += storage[M-1][i] == init_amount

# Solve the problem
problem.solve()

# Extract solution
buy_solution = [[buy_quantity[m][i].varValue for i in oils] for m in months]
refine_solution = [[refine_quantity[m][i].varValue for i in oils] for m in months]
storage_solution = [[storage[m][i].varValue for i in oils] for m in months]

output = {
    "buy": buy_solution,
    "refine": refine_solution,
    "storage": storage_solution
}

# Print the output
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')