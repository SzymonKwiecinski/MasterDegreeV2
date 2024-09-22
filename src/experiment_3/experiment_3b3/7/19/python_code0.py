import pulp
import json

# Data provided in JSON format
data_json = '''{
    "buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    "sell_price": 150,
    "is_vegetable": [true, true, false, false, false],
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
}'''

data = json.loads(data_json)

# Parameters
I = len(data['buy_price'])  # Number of oil types
M = len(data['buy_price'][0])  # Number of months

# Problem
problem = pulp.LpProblem("Oil_Refining", pulp.LpMaximize)

# Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0)
y = pulp.LpVariable.dicts("y", (range(I), range(M)), cat='Binary')

# Objective function
problem += pulp.lpSum(data['sell_price'] * refine[i][m] 
                      - data['buy_price'][i][m] * buyquantity[i][m]
                      - data['storage_cost'] * storage[i][m]
                      for i in range(I) for m in range(M))

# Constraints
for m in range(M):
    # Production constraints
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']
    
    # Hardness constraints
    refine_sum = pulp.lpSum(refine[i][m] for i in range(I))
    if refine_sum > 0:
        problem += pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) >= data['min_hardness'] * refine_sum
        problem += pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) <= data['max_hardness'] * refine_sum
    
    # Oil usage limit
    problem += pulp.lpSum(y[i][m] for i in range(I)) <= 3

for i in range(I):
    for m in range(M):
        # Storage constraints
        if m == 0:
            problem += storage[i][m] == data['init_amount'] + buyquantity[i][m] - refine[i][m]
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]

        # Usage constraints
        problem += refine[i][m] >= data['min_usage'] * y[i][m]
        
        # Storage size limit
        problem += storage[i][m] <= data['storage_size']

for m in range(M):
    for i in range(I):
        for j in range(I):
            # Dependency constraints
            if data['dependencies'][i][j] > 0:
                problem += refine[j][m] >= data['dependencies'][i][j] * refine[i][m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')