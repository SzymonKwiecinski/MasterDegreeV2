import pulp

# Problem Data
data = {
    'buy_price': [[110, 120, 130, 110, 115],
                  [130, 130, 110, 90, 115],
                  [110, 140, 130, 100, 95],
                  [120, 110, 120, 120, 125],
                  [100, 120, 150, 110, 105],
                  [90, 100, 140, 80, 135]], 
    'sell_price': 150, 
    'is_vegetable': [True, True, False, False, False], 
    'max_vegetable_refining_per_month': 200, 
    'max_non_vegetable_refining_per_month': 250, 
    'storage_size': 1000, 
    'storage_cost': 5, 
    'max_hardness': 6, 
    'min_hardness': 3, 
    'hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 
    'init_amount': 500, 
    'min_usage': 20, 
    'dependencies': [[0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0]]
}

# Constants
buy_price = data["buy_price"]
sell_price = data["sell_price"]
is_vegetable = data["is_vegetable"]
max_veg = data["max_vegetable_refining_per_month"]
max_non_veg = data["max_non_vegetable_refining_per_month"]
storage_size = data["storage_size"]
storage_cost = data["storage_cost"]
max_hardness = data["max_hardness"]
min_hardness = data["min_hardness"]
hardness = data["hardness"]
init_amount = data["init_amount"]
min_usage = data["min_usage"]
dependencies = data["dependencies"]

# Dimensions
M = len(buy_price)
I = len(buy_price[0])

# Decision variables
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

buy = pulp.LpVariable.dicts("Buy", ((m, i) for m in range(M) for i in range(I)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", ((m, i) for m in range(M) for i in range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((m, i) for m in range(M+1) for i in range(I)), lowBound=0)

# Objective Function
profit = pulp.lpSum([sell_price * pulp.lpSum(refine[m, i] for i in range(I)) -
                     pulp.lpSum(buy[m, i] * buy_price[m][i] for i in range(I)) -
                     storage_cost * pulp.lpSum(storage[m+1, i] for i in range(I))
                     for m in range(M)])
problem += profit

# Initial storage
for i in range(I):
    problem += storage[0, i] == init_amount

# End of period storage must equal initial amount
for i in range(I):
    problem += storage[M, i] == init_amount

# Refining capacity constraints
for m in range(M):
    problem += pulp.lpSum(refine[m, i] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[m, i] for i in range(I) if not is_vegetable[i]) <= max_non_veg

# Storage Constraints
for m in range(M):
    for i in range(I):
        problem += storage[m+1, i] == storage[m, i] + buy[m, i] - refine[m, i]

# Storage limit per raw oil
for m in range(1, M+1):
    for i in range(I):
        problem += storage[m, i] <= storage_size

# Hardness constraints
for m in range(M):
    hardness_expr = pulp.lpSum(refine[m, i] * hardness[i] for i in range(I))
    total_refined = pulp.lpSum(refine[m, i] for i in range(I))
    problem += hardness_expr >= min_hardness * total_refined
    problem += hardness_expr <= max_hardness * total_refined

# Maximum number of oils constraint
for m in range(M):
    oils_used = pulp.LpVariable.dicts(f"OilsUsed_{m}", (i for i in range(I)), cat='Binary')
    for i in range(I):
        problem += refine[m, i] >= min_usage * oils_used[i]
        problem += refine[m, i] <= max(0, pulp.lpSum(refine[m, j] for j in range(I))) * oils_used[i]
    problem += pulp.lpSum(oils_used[i] for i in range(I)) <= 3

# Dependency constraints
for m in range(M):
    for i in range(I):
        for j in range(I):
            if dependencies[i][j] == 1:
                problem += oils_used[i] <= oils_used[j]

# Solve the problem
problem.solve()

# Extract results
buyquantity = [[buy[m, i].varValue for i in range(I)] for m in range(M)]
refinequantity = [[refine[m, i].varValue for i in range(I)] for m in range(M)]
storagequantity = [[storage[m, i].varValue for i in range(I)] for m in range(M+1)]

print({
    "buy": buyquantity,
    "refine": refinequantity,
    "storage": storagequantity
})

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')