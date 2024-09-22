import pulp
import json

# Load data from JSON format
data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

# Define the problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Data extraction
I = len(data['buy_price'])  # number of oils
M = len(data['buy_price'][0])  # number of months

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(M)) \
           - pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] for i in range(I) for m in range(M)) \
           - pulp.lpSum(data['storage_cost'] * storage[i, m] for i in range(I) for m in range(M))

# Constraints
# 1. Refining Capacity
for m in range(M):
    problem += pulp.lpSum(refine[i, m] * int(data['is_vegetable'][i]) for i in range(I)) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] * (1 - int(data['is_vegetable'][i])) for i in range(I)) <= data['max_non_vegetable_refining_per_month']

# 2. Storage Update
for m in range(1, M):
    for i in range(I):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]
for i in range(I):
    problem += storage[i, 0] == data['init_amount']
    problem += storage[i, M-1] == data['init_amount']

# 3. Hardness Constraint
for m in range(M):
    problem += (data['min_hardness'] <= pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) /
                pulp.lpSum(refine[i, m] for i in range(I))) 
    problem += (pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) /
                pulp.lpSum(refine[i, m] for i in range(I)) <= data['max_hardness'])

# 4. Oil Usage
for m in range(M):
    for i in range(I):
        problem += refine[i, m] >= data['min_usage'] * pulp.LpVariable(f'y_{i}_{m}', 0, 1)
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += pulp.LpVariable(f'y_{i}_{m}', 0, 1) <= pulp.LpVariable(f'y_{j}_{m}', 0, 1)

# 5. Oil Usage Limit
for m in range(M):
    problem += pulp.lpSum(pulp.LpVariable(f'y_{i}_{m}', 0, 1) for i in range(I)) <= 3

# 6. Storage Capacity
for i in range(I):
    for m in range(M):
        problem += storage[i, m] <= data['storage_size']

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')