import pulp

# Data from JSON
buy_price = [[110, 120, 130, 110, 115], 
             [130, 130, 110, 90, 115], 
             [110, 140, 130, 100, 95], 
             [120, 110, 120, 120, 125], 
             [100, 120, 150, 110, 105], 
             [90, 100, 140, 80, 135]]

sell_price = 150
is_vegetable = [True, True, False, False, False]
max_vegetable_refining_per_month = 200
max_non_vegetable_refining_per_month = 250
storage_size = 1000
storage_cost = 5
min_hardness = 3
max_hardness = 6
hardness = [8.8, 6.1, 2.0, 4.2, 5.0]
init_amount = 500
min_usage = 20
dependencies = [[0, 0, 0, 0, 1], 
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0]]

# Constants
I = 5  # Number of oils
M = 5  # Number of months

# Problem definition
problem = pulp.LpProblem("Oil_Refinery_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("Used", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    sell_price * pulp.lpSum(refine[i, m] for i in range(I)) 
    - pulp.lpSum(buy_price[i][m] * buyquantity[i, m] for i in range(I)) 
    - storage_cost * pulp.lpSum(storage[i, m] for i in range(I))
    for m in range(M)
)

# Constraints

# Storage Update
for i in range(I):
    for m in range(1, M+1):
        problem += (storage[i, m] == storage[i, m-1] + buyquantity[i, m-1] - refine[i, m-1])

# Initial Storage
for i in range(I):
    problem += (storage[i, 0] == init_amount)

# Final Storage Condition
for i in range(I):
    problem += (storage[i, M] == init_amount)

# Refining Capacity
for m in range(M):
    problem += (pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_vegetable_refining_per_month)
    problem += (pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_vegetable_refining_per_month)

# Hardness Constraint
for m in range(M):
    problem += (pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) >= min_hardness * pulp.lpSum(refine[i, m] for i in range(I)))
    problem += (pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) <= max_hardness * pulp.lpSum(refine[i, m] for i in range(I)))

# Oil Usage
for i in range(I):
    for m in range(M):
        problem += (refine[i, m] >= min_usage * y[i, m])

# Dependency Constraints
for i in range(I):
    for j in range(I):
        if dependencies[i][j] == 1:
            for m in range(M):
                problem += (refine[i, m] <= max_non_vegetable_refining_per_month * y[j, m])

# Oil Count Constraint
for m in range(M):
    problem += (pulp.lpSum(y[i, m] for i in range(I)) <= 3)

# Storage Capacity
for i in range(I):
    for m in range(M+1):
        problem += (storage[i, m] <= storage_size)

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')