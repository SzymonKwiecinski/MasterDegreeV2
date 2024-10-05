import pulp

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Data input
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

M = data["M"]
I = data["I"]
buy_price = data["BuyPrice"]
sell_price = data["SellPrice"]
is_vegetable = data["IsVegetable"]
max_veg = data["MaxVegetableRefiningPerMonth"]
max_non_veg = data["MaxNonVegetableRefiningPerMonth"]
storage_size = data["StorageSize"]
storage_cost = data["StorageCost"]
min_hardness = data["MinHardness"]
max_hardness = data["MaxHardness"]
hardness = data["Hardness"]
init_amount = data["InitialAmount"]

# Decision Variables
buy = [[pulp.LpVariable(f"buy_{i}_{m}", lowBound=0) for i in range(I)] for m in range(M)]
refine = [[pulp.LpVariable(f"refine_{i}_{m}", lowBound=0) for i in range(I)] for m in range(M)]
storage = [[pulp.LpVariable(f"storage_{i}_{m}", lowBound=0, upBound=storage_size) for i in range(I)] for m in range(M+1)]

# Initial storage condition (Month 0)
for i in range(I):
    problem += storage[0][i] == init_amount

# Adding constraints for each month
for m in range(M):
    # Vegetable and non-vegetable refining constraints
    problem += pulp.lpSum(refine[m][i] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[m][i] for i in range(I) if not is_vegetable[i]) <= max_non_veg
    
    # Storage balance constraints
    for i in range(I):
        problem += storage[m + 1][i] == storage[m][i] + buy[m][i] - refine[m][i]
    
    # Product hardness constraints
    if pulp.lpSum(refine[m][i] for i in range(I)) > 0:
        avg_hardness = pulp.lpSum(hardness[i] * refine[m][i] for i in range(I)) / pulp.lpSum(refine[m][i] for i in range(I))
        problem += avg_hardness >= min_hardness
        problem += avg_hardness <= max_hardness

# End of period storage should equal initial storage
for i in range(I):
    problem += storage[M][i] == init_amount

# Objective function
revenue = pulp.lpSum(refine[m][i] * sell_price for i in range(I) for m in range(M))
cost_buy = pulp.lpSum(buy[m][i] * buy_price[m][i] for i in range(I) for m in range(M))
cost_storage = pulp.lpSum(storage[m][i] * storage_cost for i in range(I) for m in range(1, M+1))
profit = revenue - cost_buy - cost_storage
problem += profit

# Solve the problem
problem.solve()

# Extract results
result = {
    "buy": [[pulp.value(buy[m][i]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[m][i]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[m][i]) for i in range(I)] for m in range(1, M+1)]
}

# Print results
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')