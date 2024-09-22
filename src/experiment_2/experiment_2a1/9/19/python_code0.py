import pulp
import json

# Input data
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 
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
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

# Constants
I = len(data['buy_price'][0])  # Number of oils
M = len(data['buy_price'])       # Number of months

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("Buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(data['sell_price'] * pulp.lpSum(refine[i][m] for i in range(I)) for m in range(M)) \
                   - pulp.lpSum(data['buy_price'][m][i] * buyquantity[i][m] for i in range(I) for m in range(M)) \
                   - pulp.lpSum(data['storage_cost'] * storage[i][m] for i in range(I) for m in range(M))
problem += profit

# Constraints
# Monthly refining constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Storage constraints and initial conditions
for i in range(I):
    # Storage balance
    for m in range(M):
        if m == 0:
            problem += storage[i][m] == data['init_amount']
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m-1] - refine[i][m-1]
            if m == M - 1:
                problem += storage[i][m] == data['init_amount']

# Hardness constraints
for m in range(M):
    problem += (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I))) >= data['min_hardness']
    problem += (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I))) <= data['max_hardness']

# Minimum usage constraints and dependencies
for m in range(M):
    for i in range(I):
        if data['dependencies'][i].count(1) > 0:
            problem += refine[i][m] >= data['min_usage'] * pulp.lpSum(refine[j][m] for j in range(I) if data['dependencies'][i][j] == 1)

# Solve the problem
problem.solve()

# Output results
output = {
    "buy": [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)],
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')