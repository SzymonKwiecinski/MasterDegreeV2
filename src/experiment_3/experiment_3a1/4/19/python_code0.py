import pulp
import json

# Load data from JSON format
data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

# Define problem
problem = pulp.LpProblem("Oil_Refining_And_Blending", pulp.LpMaximize)

# Indices
I = len(data['buy_price'])  # Number of oil types
M = len(data['buy_price'][0])  # Number of months

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", (range(I), range(M)), cat='Binary')

# Objective Function
problem += M * data['sell_price'] - pulp.lpSum(data['buy_price'][i][m] * buyquantity[i][m] + data['storage_cost'] * storage[i][m] for i in range(I) for m in range(M))

# Constraints
for i in range(I):
    for m in range(M):
        # Storage Constraints
        if m == 0:
            problem += storage[i][m] == data['init_amount']  # Initial Storage
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]  # Storage equation
    # Final Storage constraint
    problem += storage[i][M-1] == data['init_amount']

# Refining Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Hardness Constraint
for m in range(M):
    problem += (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / 
                 pulp.lpSum(refine[i][m] for i in range(I) if refine[i][m] > 0)) >= data['min_hardness'])
    problem += (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / 
                 pulp.lpSum(refine[i][m] for i in range(I) if refine[i][m] > 0)) <= data['max_hardness'])

# Oil Usage Constraints
for i in range(I):
    for m in range(M):
        problem += refine[i][m] >= data['min_usage'] * y[i][m]

# Dependency Constraints
for i in range(I):
    for j in range(I):
        if data['dependencies'][i][j] == 1:
            for m in range(M):
                problem += refine[j][m] >= data['min_usage'] * y[i][m]

# Oil Selection Constraint
for m in range(M):
    problem += pulp.lpSum(y[i][m] for i in range(I)) <= 3

# Solve problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')