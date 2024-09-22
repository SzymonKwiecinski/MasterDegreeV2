import pulp
import json

# Data in JSON format
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

# Parameters
I = len(data['is_vegetable'])  # number of oil types
M = len(data['buy_price'][0])   # number of months

# Create the problem
problem = pulp.LpProblem("Oil_Refining_and_Blending", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0)

# Objective function
problem += (data['sell_price'] * pulp.lpSum(refine[i][m] for i in range(I) for m in range(M)) - 
             pulp.lpSum(data['buy_price'][i][m] * buyquantity[i][m] for i in range(I) for m in range(M)) - 
             data['storage_cost'] * pulp.lpSum(storage[i][m] for i in range(I) for m in range(M)))

# Constraints
for m in range(M):
    problem += (pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month'])
    problem += (pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month'])
    
for i in range(I):
    for m in range(1, M):
        problem += (storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m])

for i in range(I):
    for m in range(M):
        problem += (storage[i][m] <= data['storage_size'])

for i in range(I):
    problem += (storage[i][M-1] == data['init_amount'])

for i in range(I):
    for m in range(M):
        problem += (pulp.lpSum(refine[j][m] for j in range(I) if data['dependencies'][i][j]) >= data['min_usage'] * refine[i][m])

for m in range(M):
    problem += (data['max_hardness'] >= (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / 
                                          pulp.lpSum(refine[i][m] for i in range(I))) >= data['min_hardness'])

for m in range(M):
    problem += (pulp.lpSum(refine[i][m] for i in range(I)) <= 3)

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')