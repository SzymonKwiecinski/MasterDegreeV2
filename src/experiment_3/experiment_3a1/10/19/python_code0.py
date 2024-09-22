import pulp
import json

# Data from the provided JSON
data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

# Extracting data
buy_price = data['buy_price']
sell_price = data['sell_price']
is_vegetable = data['is_vegetable']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_cost = data['storage_cost']
min_hardness = data['min_hardness']
max_hardness = data['max_hardness']
hardness = data['hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
dependencies = data['dependencies']

# Setting up problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Sets
I = range(len(buy_price))  # Oils
M = range(len(buy_price[0]))  # Months

# Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (I, M), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (I, M), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (I, M), lowBound=0)

# Objective Function
profit = pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in I) - 
                    pulp.lpSum(buy_price[i][m] * buyquantity[i][m] for i in I) - 
                    storage_cost * pulp.lpSum(storage[i][m] for i in I) for m in M)

problem += profit, "Total_Profit"

# Constraints
# Storage Constraints
for i in I:
    for m in M:
        if m == 0:
            problem += storage[i][m] == init_amount, f"Storage_Initial_{i}"
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"Storage_Update_{i}_{m}"

# Refining Capacity Constraints
for m in M:
    problem += pulp.lpSum(refine[i][m] for i in I if is_vegetable[i]) <= max_veg, f"Max_Vegetable_Refining_{m}"
    problem += pulp.lpSum(refine[i][m] for i in I if not is_vegetable[i]) <= max_non_veg, f"Max_Non_Vegetable_Refining_{m}"

# Hardness Constraints
for m in M:
    total_refine = pulp.lpSum(refine[i][m] for i in I)
    problem += min_hardness <= pulp.lpSum(hardness[i] * refine[i][m] for i in I) / (total_refine + 1e-5), f"Min_Hardness_{m}"
    problem += pulp.lpSum(hardness[i] * refine[i][m] for i in I) / (total_refine + 1e-5) <= max_hardness, f"Max_Hardness_{m}"

# Usage Constraints
for i in I:
    for m in M:
        problem += refine[i][m] >= min_usage * pulp.lpVariable(f"is_used_{i}_{m}", cat='Binary'), f"Min_Usage_{i}_{m}"

# Dependency Constraints
for i in I:
    for j in I:
        if dependencies[i][j] != 0:
            for m in M:
                problem += refine[j][m] >= min_usage * dependencies[i][j] * pulp.lpVariable(f"is_used_{i}_{m}", cat='Binary'), f"Dependency_{i}_{j}_{m}"

# Oil Usage Limit
for m in M:
    problem += pulp.lpSum(pulp.lpVariable(f"is_used_{i}_{m}", cat='Binary') for i in I) <= 3, f"Max_Oil_Usage_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')