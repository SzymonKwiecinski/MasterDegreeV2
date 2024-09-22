import pulp
import json

# Load data from the provided JSON format
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], 
                  [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'sell_price': 150,
    'is_vegetable': [True, True, False, False, False],
    'max_vegetable_refining_per_month': 200,
    'max_non_vegetable_refining_per_month': 250,
    'storage_size': 1000,
    'storage_cost': 5,
    'min_hardness': 3,
    'max_hardness': 6,
    'hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'init_amount': 500,
    'min_usage': 20,
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

# Define indices
I = len(data['buy_price'])  # number of oil types
M = len(data['buy_price'][0])  # number of months

# Create the Linear Program
problem = pulp.LpProblem("Oil_Refining_and_Blend", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", (range(I), range(M + 1)), lowBound=0)
y = pulp.LpVariable.dicts("Usage", (range(I), range(M)), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['sell_price'] * refine[i][m] for i in range(I) for m in range(M)) - \
           pulp.lpSum(data['buy_price'][i][m] * buyquantity[i][m] for i in range(I) for m in range(M)) - \
           pulp.lpSum(data['storage_cost'] * storage[i][m] for i in range(I) for m in range(M))

# Constraints
# Production Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Storage Constraints
for i in range(I):
    problem += storage[i][0] == data['init_amount']
for i in range(I):
    for m in range(1, M):
        problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]
for i in range(I):
    problem += storage[i][M] == data['init_amount'] 

# Hardness Constraints
for m in range(M):
    problem += pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) >= data['min_hardness'] * pulp.lpSum(refine[i][m] for i in range(I))
    problem += pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) <= data['max_hardness'] * pulp.lpSum(refine[i][m] for i in range(I))

# Usage Constraints
for i in range(I):
    for m in range(M):
        problem += refine[i][m] >= data['min_usage'] * y[i][m]

# Dependency Constraints
for i in range(I):
    for j in range(I):
        problem += refine[j][m] <= data['dependencies'][i][j] * refine[i][m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')