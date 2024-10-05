import pulp

# Data
data = {
    "buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    "sell_price": 150,
    "is_vegetable": [True, True, False, False, False],
    "max_vegetable_refining_per_month": 200,
    "max_non_vegetable_refining_per_month": 250,
    "storage_size": 1000,
    "storage_cost": 5,
    "min_hardness": 3,
    "max_hardness": 6,
    "hardness": [8.8, 6.1, 2.0, 4.2, 5.0],
    "init_amount": 500,
    "min_usage": 20,
    "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

# Parameters
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

I = len(is_vegetable)  # Number of oils
M = len(buy_price)     # Number of months

# Model
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Variables
buy = pulp.LpVariable.dicts("Buy", (range(M), range(I)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", (range(M), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(M+1), range(I)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("Use", (range(M), range(I)), cat='Binary')

# Initial storage
for i in range(I):
    problem += storage[0][i] == init_amount

# Constraints
for m in range(M):
    vegetable_refining = pulp.lpSum(refine[m][i] for i in range(I) if is_vegetable[i])
    non_vegetable_refining = pulp.lpSum(refine[m][i] for i in range(I) if not is_vegetable[i])
    
    problem += vegetable_refining <= max_veg
    problem += non_vegetable_refining <= max_non_veg

    for i in range(I):
        problem += storage[m+1][i] == storage[m][i] + buy[m][i] - refine[m][i]
        problem += storage[m+1][i] <= storage_size
        
        # Minimum usage constraint
        problem += refine[m][i] >= min_usage * use[m][i]
        
        # Enforcing dependency constraints
        for j in range(I):
            if dependencies[i][j] == 1:
                problem += use[m][i] <= use[m][j]

    # Limiting to use at most 3 oils in any month
    problem += pulp.lpSum(use[m][i] for i in range(I)) <= 3

    # Hardness constraints
    total_refine = pulp.lpSum(refine[m][i] for i in range(I))
    if total_refine > 0:
        weighted_hardness = pulp.lpSum(hardness[i] * refine[m][i] for i in range(I)) / total_refine
        problem += weighted_hardness <= max_hardness
        problem += weighted_hardness >= min_hardness

# End of period storage must be equal to initial
for i in range(I):
    problem += storage[M][i] == init_amount

# Objective
revenue = pulp.lpSum(sell_price * pulp.lpSum(refine[m][i] for i in range(I)) for m in range(M))
cost_buy = pulp.lpSum(buy_price[m][i] * buy[m][i] for m in range(M) for i in range(I))
cost_storage = pulp.lpSum(storage_cost * storage[m][i] for m in range(M) for i in range(I))

problem += revenue - cost_buy - cost_storage

# Solve
problem.solve()

# Output
buyquantity_output = [[pulp.value(buy[m][i]) for i in range(I)] for m in range(M)]
refine_output = [[pulp.value(refine[m][i]) for i in range(I)] for m in range(M)]
storage_output = [[pulp.value(storage[m][i]) for i in range(I)] for m in range(M+1)]

output = {
    "buy": buyquantity_output,
    "refine": refine_output,
    "storage": storage_output
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')