import pulp

# Data
buy_price = [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]]
sell_price = 150
is_vegetable = [True, True, False, False, False, False]
max_veg = 200
max_non_veg = 250
storage_size = 1000
storage_cost = 5
min_hardness = 3
max_hardness = 6
hardness = [8.8, 6.1, 2.0, 4.2, 5.0, 3.5]
init_amount = 500
min_usage = 20
dependencies = [[0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

# Problem
problem = pulp.LpProblem("Food_Manufacturing_Problem", pulp.LpMaximize)

# Sets
I = range(len(buy_price))  # Oils
M = range(len(buy_price[0]))  # Months

# Decision Variables
buy = pulp.LpVariable.dicts("Buy", ((i, m) for i in I for m in M), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in I for m in M), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in I for m in M), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("Use", ((i, m) for i in I for m in M), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    sell_price * pulp.lpSum(refine[i, m] for i in I) - 
    pulp.lpSum(buy_price[i][m] * buy[i, m] + storage_cost * storage[i, m] for i in I) 
    for m in M
)

# Constraints
# Inventory balance
for i in I:
    for m in M:
        if m == 0:
            problem += storage[i, m] == init_amount + buy[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m-1] + buy[i, m] - refine[i, m]

# Final storage requirement
for i in I:
    problem += storage[i, len(M) - 1] == init_amount

# Storage capacity constraint
for i in I:
    for m in M:
        problem += storage[i, m] <= storage_size

# Refining capacity constraints
for m in M:
    problem += pulp.lpSum(refine[i, m] for i in I if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[i, m] for i in I if not is_vegetable[i]) <= max_non_veg

# Hardness constraint
for m in M:
    total_refine = pulp.lpSum(refine[i, m] for i in I)
    problem += (total_refine > 0)  # Added condition to ensure proper syntax
    problem += pulp.lpSum((refine[i, m] * hardness[i]) / total_refine for i in I if total_refine > 0) <= max_hardness
    problem += pulp.lpSum((refine[i, m] * hardness[i]) / total_refine for i in I if total_refine > 0) >= min_hardness

# Usage constraints
for i in I:
    for m in M:
        problem += refine[i, m] >= min_usage * use[i, m]

# At most three oils can be used
for m in M:
    problem += pulp.lpSum(use[i, m] for i in I) <= 3

# Dependency constraints
for i in I:
    for j in I:
        if dependencies[i][j] == 1:
            for m in M:
                problem += use[i, m] <= use[j, m] + 1 - dependencies[i][j]

# Solve the problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')