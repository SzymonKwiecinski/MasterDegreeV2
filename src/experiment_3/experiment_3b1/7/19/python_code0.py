import pulp
import json

# Load data
data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

# Constants and parameters
M = len(data['buy_price'][0])  # Number of months
I = len(data['buy_price'])  # Number of oils
sell_price = data['sell_price']

# Create problem
problem = pulp.LpProblem("Oil_Refining_Profit_Maximization", pulp.LpMaximize)

# Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0)

# Objective Function
profit = pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in range(I)) - 
                    pulp.lpSum(data['buy_price'][i][m] * buyquantity[i][m] for i in range(I)) - 
                    data['storage_cost'] * pulp.lpSum(storage[i][m] for i in range(I)) 
                    for m in range(M))

problem += profit

# Constraints
# Refining Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Storage Capacity Constraint
for i in range(I):
    for m in range(M):
        problem += storage[i][m] <= data['storage_size']

# Hardness Constraints
for m in range(M):
    total_refine = pulp.lpSum(refine[i][m] for i in range(I))
    problem += data['min_hardness'] <= (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / total_refine) <= data['max_hardness']

# Initial and Final Storage Constraints
for i in range(I):
    problem += storage[i][0] == data['init_amount']
    problem += storage[i][M-1] == data['init_amount']

# Storage Update Constraints
for m in range(1, M):
    for i in range(I):
        problem += storage[i][m] == storage[i][m - 1] + buyquantity[i][m] - refine[i][m]

# Minimum Usage Constraints
delta = pulp.LpVariable.dicts("delta", (range(I), range(M)), cat='Binary')
for m in range(M):
    for i in range(I):
        problem += refine[i][m] >= data['min_usage'] * delta[i][m]

# Dependency Constraints
for m in range(M):
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += refine[j][m] >= delta[i][m] * refine[i][m]

# Three Oil Limit Constraint
for m in range(M):
    problem += pulp.lpSum(delta[i][m] for i in range(I)) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')