import pulp
import json

# Load data from the JSON format
data = json.loads("""{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}""")

# Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
I = len(data['buy_price'])  # Number of items
M = 5  # Number of months

refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("use", (range(I), range(M)), cat='Binary')

# Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i][m] - 
                    data['buy_price'][i][m] * buyquantity[i][m] - 
                    data['storage_cost'] * storage[i][m] 
                    for i in range(I) for m in range(M))

problem += profit

# Constraints
# Balance Constraints
for i in range(I):
    for m in range(1, M):
        problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]

# Initial storage
for i in range(I):
    problem += storage[i][0] == data['init_amount']

# Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Storage Constraints
for i in range(I):
    for m in range(M):
        problem += storage[i][m] <= data['storage_size']

# Hardness Constraints
for m in range(M):
    problem += pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) >= data['min_hardness'] * pulp.lpSum(refine[i][m] for i in range(I))
    problem += pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) <= data['max_hardness'] * pulp.lpSum(refine[i][m] for i in range(I))

# Usage Constraints
for m in range(M):
    problem += pulp.lpSum(use[i][m] for i in range(I)) <= 3
    for i in range(I):
        problem += refine[i][m] >= data['min_usage'] * use[i][m]
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += pulp.lpSum(use[j][m] for j in range(I)) >= use[i][m]

# Final Storage Constraint
for i in range(I):
    problem += storage[i][M-1] == data['init_amount']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')