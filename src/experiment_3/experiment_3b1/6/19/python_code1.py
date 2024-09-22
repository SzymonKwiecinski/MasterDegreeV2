import pulp
import json

# Data input
data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

# Parameter Extraction
buy_price = data['buy_price']
sell_price = data['sell_price']
is_vegetable = data['is_vegetable']
max_vegetable = data['max_vegetable_refining_per_month']
max_non_vegetable = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
min_hardness = data['min_hardness']
max_hardness = data['max_hardness']
hardness = data['hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
dependencies = data['dependencies']

# Sets
I = range(len(is_vegetable))  # set of oils
M = range(len(buy_price[0]))   # set of months

# Create the problem
problem = pulp.LpProblem("Oil_Refining_Blend", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (I, M), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (I, M), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (I, M), lowBound=0)

# Objective Function
problem += pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in I) - 
                      pulp.lpSum(buy_price[i][m] * buyquantity[i][m] for i in I) - 
                      storage_cost * pulp.lpSum(storage[i][m] for i in I) for m in M)

# Constraints
for m in M:
    problem += pulp.lpSum(refine[i][m] for i in I if is_vegetable[i]) <= max_vegetable, f"Veg_Refine_Constraint_{m}"
    problem += pulp.lpSum(refine[i][m] for i in I if not is_vegetable[i]) <= max_non_vegetable, f"NonVeg_Refine_Constraint_{m}"

for i in I:
    for m in M:
        if m == 0:
            problem += storage[i][m] == init_amount + buyquantity[i][m] - refine[i][m], f"Storage_Initial_{i}_{m}"
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"Storage_Constraint_{i}_{m}"
        problem += storage[i][m] <= storage_size, f"Storage_Size_Constraint_{i}_{m}"
        problem += storage[i][m] >= 0, f"Non_Negative_Storage_{i}_{m}"

for m in M:
    problem += (pulp.lpSum(refine[i][m] * hardness[i] for i in I) / 
                 (pulp.lpSum(refine[i][m] for i in I) + 1e-5) >= min_hardness, 
                 f"Min_Hardness_Constraint_{m}")
    
    problem += (pulp.lpSum(refine[i][m] * hardness[i] for i in I) / 
                 (pulp.lpSum(refine[i][m] for i in I) + 1e-5) <= max_hardness, 
                 f"Max_Hardness_Constraint_{m}")

for m in M:
    for i in I:
        problem += refine[i][m] >= min_usage * (buyquantity[i][m] > 0), f"Min_Usage_Constraint_{i}_{m}"

for m in M:
    for j in I:
        problem += refine[j][m] <= pulp.lpSum(dependencies[i][j] * refine[i][m] for i in I), f"Dependency_Constraint_{j}_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')